import socket
import traceback  # For detailed error reporting
import threading
import json
import sys
from metainfo import read_metainfo
from server_data import add_peer, add_shared_file, get_peers_for_file, remove_peer


peerlist = {}  
file_sharing = {}  


def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    try:
        while True:
            message = client_socket.recv(4096).decode("utf-8")
            if not message:
                break
            print(f"Received from {client_address}: {message}")
            data = json.loads(message)
            #response
            if data['action'] == 'introduce':
                peer_port = data['peer_port']
                peer_name = data['peer_name']
                peer_id = data['peer_id']
                add_peer(peer_id, peer_name, peer_port)
                print(f"add {peer_name} to connection")
            
            if data['action'] == 'publish':
                peer_port = data['peer_port']
                peer_name = data['peer_name']
                peer_id = data['peer_id']
                file_name = data['file_name']
                metainfo = data['metainfo']
                
                flag = add_shared_file(peer_id, file_name)
                if flag == 1:
                    response = 'file been publish successfully'
                if flag == 0:
                    response = 'file have been there before'
                
                client_socket.sendall(response.encode("utf-8"))
                
            if data['action'] == 'fetch':
                peer_port = data['peer_port']
                peer_name = data['peer_name']
                peer_id = data['peer_id']
                file_name = data['file_name']
                
                metainfo = data.get('metainfo')
                if not metainfo:
                    peer_have_file = get_peers_for_file(file_name)
                    
                    client_socket.sendall(json.dumps(peer_have_file).encode()+ b'\n')
                else:
                    read_metainfo(metainfo)
                                                  
    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        print(f"Closing connection with {client_address}")
        if peer_id:
            remove_peer(peer_id)  # Xóa peer và file của peer đó
        client_socket.close()
    

def server(host, port):
    # handling server + multithread
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Server started and is listening for connections.")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()

    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        server_socket.close()
        # client_socket.close()


if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    # server_thread = threading.Thread(target=server,args=(host, port))
    # server_thread.start()
    # sys.exit(0)
    server(host, port)