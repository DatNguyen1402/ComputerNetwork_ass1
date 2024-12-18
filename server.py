import socket
import traceback  # For detailed error reporting
import threading
import json
import sys
from server_data import add_peer, add_shared_file, get_peers_for_file, remove_peer, getmetainfo, peerlist, file_sharing, file_metadata



def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    try:
        while True:
            message = client_socket.recv(4096).decode("utf-8")
            if not message:
                break
            print(f"Recieve messege : {message} ")
            data = json.loads(message)
            #response
            if data['action'] == 'introduce':
                peer_port = data['peer_port']
                peer_name = data['peer_name']
                peer_id = data['peer_id']
                peer_ip = data['peer_ip']
                add_peer(peer_id, peer_name, peer_ip, peer_port)
                
                print(f"add {peer_name}, id :{peer_id}, ip :{peer_ip}, port : {peer_port} to connection")
            
            if data['action'] == 'publish':
                peer_port = data['peer_port']
                peer_ip = data['peer_ip']
                peer_name = data['peer_name']
                peer_id = data['peer_id']
                file_name = data['file_name']
                metainfo = data['metainfo']
                
                flag = add_shared_file(peer_id, file_name, metainfo)
                if flag == 1:
                    response = 'Response from server : File been publish successfully'
                if flag == 0:
                    response = 'Response from server : File have been published before'
                
                client_socket.sendall(response.encode("utf-8"))
                
            if data['action'] == 'fetch':
                peer_port = data['peer_port']
                peer_name = data['peer_name']
                peer_id = data['peer_id']
                peer_ip = data['peer_ip']
                file_name = data['file_name']
                
                peer_have_file = get_peers_for_file(file_name)
                
                if not peer_have_file:
                    response = "None"
                    client_socket.sendall(response.encode())
                else:    
                    metainfo = getmetainfo(file_name, file_metadata)
                        
                    response = {'peer_list' : peer_have_file,
                                'metainfo' : metainfo}
                    
                    client_socket.sendall(json.dumps(response).encode()+ b'\n')
                
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
    print("Server started and is listening for connections...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            thread.start()

    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        server_socket.close()


if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    server(host, port)