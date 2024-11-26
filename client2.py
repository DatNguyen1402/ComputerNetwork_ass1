import os
import socket
import os
import threading
import math
import json
import shlex
from metainfo import generate_metainfo

# client 2 (peer2) 

host = 'localhost'
id = 2
port = 6002
name = 'client 2'
file_dir = "../src/clients/client2/origin"
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
        if check_file_share(file_name) == 1:
            print("File have been there")
            return
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
            return        
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
    #response cần bao gồm peerlist info, metainfo của file
    print(response)
    
    
    # recieve the response from the tracker {num_peer: num, peer_list:[{host: , port: }] }
    # if num =0 -> no peer have file
    # if num>0 -> start dowload
    
    # get the metainfo from the tracker, creat the list of piece (flag, piece_order, calculate the startbyte and endbyte)
    
    
    # then, make connect to the peer
    
    # send request to peer {type: request_piece, filename, piece_order}
    
    # recieve the data, write to the 

    
def handle(peer_list):
    pass

def handle_file_request(other_sock, file_dir):
    try:
        data = other_sock.recv(4096).decode()
        # message = json.loads(data)
        
            
            # send_piece_to_client(conn, file, index)
    finally:
        other_sock.close()

def request_piece(selfsock, piece, hash, peer_host, peer_port):            
    pass


def send_piece_to_client(other_sock, metainfo, piece_index):
    pass
    




   
stop_event = threading.Event()
    
def peer_server(port, shared_files_dir):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('0.0.0.0', port))
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.listen()

    while not stop_event.is_set():
        try:
            server_sock.settimeout(1) 
            conn, addr = server_sock.accept()
            thread = threading.Thread(target=handle, args=(conn, shared_files_dir))
            thread.start()
        except socket.timeout:
            continue
        except Exception as e:
            break

    server_sock.close()
        
if __name__ == "__main__":
    server_host = 'localhost'
    server_port = 5000
    
    sock = connect_to_server(server_host, server_port)
    
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
                break
            else:
                print("Invalid command.")

    finally:
            sock.close()


 
    #print_metainfo(split_file_into_pieces(f"{file_dir}/eBook.txt",500000))