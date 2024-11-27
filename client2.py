import os
import socket
import os
import threading
import math
import json
from metainfo import generate_metainfo, parse_meta_info
from trackfile import check_file, check_file_share
from server_data import get_peerport, get_peerip
from dowload_data import generate_request, handle_file_request, request_piece, merge_pieces
import shlex


def connect_to_server(server_host, server_port):
    sock_peer_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_peer_server.connect((server_host, server_port))
    message = {
        'action' : 'introduce',
        'peer_id': id,
        'peer_name': name,
        'peer_port': port,
        'peer_ip' : ip
    }
    sock_peer_server.sendall(json.dumps(message).encode() + b'\n')
    return sock_peer_server
    
def publish(sock_peer_server,id ,port, ip, name, file_name, file_dir, file_share):
    if check_file(file_dir, file_name) == 1:
        if check_file_share(file_name, file_share) == True:
            print("system : File have been there")
        else:
            metaifo = generate_metainfo(os.path.join(file_dir, file_name), 512*1024)
            message = {
            'action' : 'publish',
            'peer_id': id,
            'peer_name': name,
            'peer_port': port,
            'peer_ip' : ip,
            'file_name': file_name,
            'metainfo' : metaifo
            }
            sock_peer_server.sendall(json.dumps(message).encode("utf-8") + b'\n')
            
            response = sock_peer_server.recv(4096).decode("utf-8")
            file_share.append(file_name)
            print(response)        
    else:
        print("system : File not found in directory, cannot publish")
        
    
def fetch(sock_peer_server, port, ip, name, id, file_data, file_dir):    #send to server
    # this request the tracker to have peerlist {type: request_file, filename : filename}
    if isinstance(file_data, str):
        file_name = file_data
        metainfo = None
    
    elif isinstance(file_data, dict):
        file_name = file_data.get('filename')
        metainfo = file_data
    
    message ={
        'action' : 'fetch',
        'peer_id': id,
        'peer_name': name,
        'peer_port': port,
        'peer_ip' : ip,
        'file_name': file_name,
        'metainfo' : metainfo
    }
    
    sock_peer_server.sendall(json.dumps(message).encode('utf-8') + b'\n')
    
    response = sock_peer_server.recv(4096).decode("utf-8")      
    response_data = json.loads(response)
    
    print(response_data)
    
    peerlist = response_data['peer_list']
    read_metainfo = parse_meta_info(response_data['metainfo'])
    
    num_pieces = read_metainfo['num_pieces'] #example            
    num_peers = len(peerlist)
    
    if num_peers == 0:
        print("Response from server : No peers have this file. ")
        return 
    if num_peers > 0:
        print(f"Response from server: {num_peers} peer(s) have this file, start download file...")
        
    print(peerlist)    

    request_list = generate_request(num_pieces, peerlist) 
    
    print(request_list)
    
    request_threads=[]

    for peer_id, piece_index in request_list:
        peer_port = get_peerport(peer_id, peerlist)
        peer_ip = get_peerip(peer_id, peerlist)
        thread = threading.Thread(target=request_piece, args=(file_dir, file_name, piece_index, peer_port, peer_ip))
        thread.start()
        request_threads.append(thread)
        # Create a thread for each piece request 
    for thread in request_threads:
        thread.join()
        
    merge_pieces(file_dir, file_name, num_pieces)

    
    
def peer_host(ip, port, file_dir):
    sock_peer_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_peer_peer.bind((ip, port))
    sock_peer_peer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_peer_peer.listen()
    while not stop_event.is_set():
        try:
            sock_peer_peer.settimeout(1) 
            peer_sock, addr = sock_peer_peer.accept()
            thread = threading.Thread(target=handle_file_request, args=(peer_sock,file_dir))
            thread.start()
        except socket.timeout:
            continue
        except Exception as e:
            break

    sock_peer_peer.close()    
   
stop_event = threading.Event()

def start_client(server_host, server_port,peer_id, peer_ip, peer_port, peer_dir, name, file_share):
        
    peer_host_thread = threading.Thread(target=peer_host, args=(peer_ip, peer_port, peer_dir))
    peer_host_thread.start()

    sock = connect_to_server(server_host, server_port)
      
    try:
        while True:
            user_input = input("Enter command (publish file_name/ fetch file_name/ exit): ")#addr[0],peers_port, peers_hostname,file_name, piece_hash,num_order_in_file
            command_parts = shlex.split(user_input)
            if len(command_parts) == 2 and command_parts[0].lower() == 'publish':
                _,file_name = command_parts
                publish(sock,peer_id,peer_port, peer_ip, name, file_name, peer_dir, file_share)
            elif len(command_parts) == 2 and command_parts[0].lower() == 'fetch':
                _, file_data = command_parts
                fetch(sock, peer_port, peer_ip, name, peer_id ,file_data, peer_dir)
            elif user_input.lower() == 'exit':
                sock.close()
                stop_event.set()
                break
            else:
                print("Invalid command.")
    except KeyboardInterrupt:
        exit(0)
    finally:
        sock.close()
        peer_host_thread.join()         
         
if __name__ == "__main__":
    server_host = 'localhost'
    server_port = 5000
    id = 2
    port = 6002
    ip = 'localhost'
    name = 'client 2'
    file_dir = "../src/clients/client2/origin"
    file_share = []     #store filename only
    start_client(server_host, server_port, id, ip, port, file_dir, name, file_share)
    
    