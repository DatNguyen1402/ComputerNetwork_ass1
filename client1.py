import os
import socket
import os
import threading
import math
import json
from metainfo import generate_metainfo, parse_meta_info
import shlex
# client 1 (peer1) 

host = 'localhost'
id = 1
port = 6001
name = 'client 1'
file_dir = "../src/clients/client1/origin"
file_share = []     #store filename only

    
def check_file_path(file_path):
    print(f"Checking in the file path {file_path}")
    if not os.path.isdir(file_path):
        print("The provided path is not a valid directory.")
        return -1
    else:
        files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
        
        if files:
            print("Files in the directory:")
            for filename in files:
                print(filename)
            return 1  
        else:
            print("Directory is empty. No files found.")
            return 0

def check_file(file_path, file_name):
    print(f"Check if {file_name} in path {file_path}")
    flag = 0
    if not os.path.isdir(file_path):
        print("The provided path is not a valid directory.")
        return -1
    else:
        files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
        
        if files:
            for filename in files:
                if file_name == filename:
                    flag = 1    
    if flag == 0:
        print("File not found")
    if flag == 1:
        print("File found in path")
    return flag

def check_file_share(file_name):
    for i in file_share: 
        if i == file_name:
            return 1 
    return 0 


def publish(sock, file_name):
    print(f"Publish {file_name} to the network")
    if check_file(file_dir, file_name) == 1:
        if check_file_share(file_name) == True:
            print("File have been there")
        else:
            metaifo = generate_metainfo(os.path.join(file_dir, file_name), 512*1024)
            message = {
            'action' : 'publish',
            'peer_id': id,
            'peer_name': name,
            'peer_port': port,
            'file_name': file_name,
            'metainfo' : metaifo
            }
            sock.sendall(json.dumps(message).encode("utf-8") + b'\n')
            
            response = sock.recv(4096).decode("utf-8")
            file_share.append(file_name)
            print(response)        
    else:
        print("File not found in directory, cannot publish")
        
def connect_to_server(server_host, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_host, server_port))
    message = {
        'action' : 'introduce',
        'peer_id': id,
        'peer_name': name,
        'peer_port': port,
    }
    sock.sendall(json.dumps(message).encode() + b'\n')
    return sock
        
    
def fetch(sock, file_data):    #send to server
    # this request the tracker to have peerlist {type: request_file, filename : filename}
    if isinstance(file_data, str):
        file_name = file_data
        metainfo = None
        print(f"Fetch {file_name} from peer {name}")
    
    elif isinstance(file_data, dict):
        file_name = file_data.get('filename')
        metainfo = file_data
        print(f"Fetch file using metainfo {metainfo}")
    
    message ={
        'action' : 'fetch',
        'peer_id': id,
        'peer_name': name,
        'peer_port': port,
        'file_name': file_name,
        'metainfo' : metainfo
    }
    
    sock.sendall(json.dumps(message).encode('utf-8') + b'\n')
    
    response = sock.recv(4096).decode("utf-8")
    
    peerlist = json.loads(response)
    
    num_peers = len(peerlist)
    
    if num_peers == 0:
        print("no peer")
        return 
    if num_peers > 0:
        print(f"have {num_peers}, start download file")
    print(peerlist)    

    num_pieces = 7 #example
    
    request_list = generate_request(num_pieces, peerlist) 
    
    print(request_list)
    
    request_threads=[]
    
    for peer_id, piece_index in request_list:
        peer_port = get_peerport(peer_id, peerlist)
        
        thread = threading.Thread(target=request_piece, args=(file_name, piece_index, peer_port))
        thread.start()
        request_threads.append(thread)
        # Create a thread for each piece request 
        for thread in request_threads:
            thread.join()

def get_peerport(peer_id, peerlist):
    for peer in peerlist:
        if peer['peer_id'] == peer_id:
            return peer['peerport']  
    return None  

def generate_request(num_pieces, peerlist):
    num_peers = len(peerlist)
    
    peer_requests = []

    for piece_index in range(num_pieces):
        peer = peerlist[piece_index % num_peers]
        peer_id = peer['peer_id']
        peer_requests.append((peer_id, piece_index))

    return peer_requests

    

def handle_file_request(other_sock):
    try:
        data = other_sock.recv(4096).decode()
        # message = json.loads(data)
        if data:
            print(f"client2 get {data}")
        message = json.loads(data)
        if message['action'] == 'send_file':
            file_name = message['file_name']
            piece_index = message['piece_index']
            send_piece_to_client(other_sock, file_name, piece_index)
    finally:
        other_sock.close()

def request_piece(file_name, piece_index, peer_port):
    try:
        peer_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        filepath = os.path.join(file_dir, file_name)
        peer_sock.connect(('localhost', peer_port))
        peer_sock.sendall(json.dumps({
            'action': 'send_file', 
            'file_name': file_name, 
            'piece_index': piece_index
        }).encode() + b'\n')

        with open(f"{filepath}_piece{piece_index}", 'wb') as f:
            while True:
                data = peer_sock.recv(4096)
                if not data:
                    break
                f.write(data)

        print(f"Downloaded piece {piece_index} of {file_name}")
    except Exception as e:
        print(f"Error downloading piece {piece_index}: {e}")
    finally:
        peer_sock.close()



def send_piece_to_client(other_sock, file_name, piece_index, piece_size=512*1024):
    file_path = os.path.join(file_dir, file_name)
    try:
        with open(file_path, 'rb') as f:
            while True:
                f.seek(piece_index * piece_size)
                data = f.read(piece_size)
        
        offset = 0
        chunk_size = 4096
        while offset < len(data):
            chunk = data[offset:offset + chunk_size]
            other_sock.sendall(chunk)
            offset += chunk_size
                
    except FileNotFoundError:
        print(f"File {file_name} not found.")
    except Exception as e:
        print(f"Error while sending piece: {e}")

    
def peer_server(port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('0.0.0.0', port))
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.listen()
    print(f"peer1 listening on {port}")
    while not stop_event.is_set():
        try:
            server_sock.settimeout(1) 
            peer_sock, addr = server_sock.accept()
            thread = threading.Thread(target=handle_file_request, args=(peer_sock,))
            thread.start()
        except socket.timeout:
            continue
        except Exception as e:
            break

    server_sock.close()    
   
stop_event = threading.Event()
        
if __name__ == "__main__":
    server_host = 'localhost'
    server_port = 5000
    port = 6001
    
    peer_server_thread = threading.Thread(target=peer_server, args=(port,))
    peer_server_thread.start()

    
    sock = connect_to_server(server_host, server_port)
    # publish('Chapter_3.pdf')
 
    #print_metainfo(split_file_into_pieces(f"{file_dir}/eBook.txt",500000))    
    try:
        while True:
            user_input = input("Enter command (publish file_name/ fetch file_name/ exit): ")#addr[0],peers_port, peers_hostname,file_name, piece_hash,num_order_in_file
            command_parts = shlex.split(user_input)
            if len(command_parts) == 2 and command_parts[0].lower() == 'publish':
                _,file_name = command_parts
                publish(sock, file_name)
            elif len(command_parts) == 2 and command_parts[0].lower() == 'fetch':
                _, file_name = command_parts
                fetch(sock,file_name)
            elif user_input.lower() == 'exit':
                sock.close()
                stop_event.set()
                break
            else:
                print("Invalid command.")

    finally:
        sock.close()
        peer_server_thread.join()