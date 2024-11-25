import socket
import traceback  # For detailed error reporting
import threading
import json

peer_list = []

class PeerInfo:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.file_share = []
        
        
    def add_file(self, filename):
        if filename not in self.file_share:
            self.file_share.append(filename)
        
    def __repr__(self):
        return f"Peer(name={self.name}, files={self.file_share})"

def add_or_update_peer(name, filename):
    for peer in peer_list:
        if peer.name == name:
            peer.add_file(filename)  
            return  

    new_peer = PeerInfo(name)
    new_peer.add_file(filename)  # Add the shared file
    peer_list.append(new_peer)

def show_peers():
    for peer in peer_list:
        print(peer)

peerlist = {}  
file_sharing = {}  

def add_peer(peer_id, peer_name, port):
    peerlist[peer_id] = {
        'peer_name': peer_name,
        'peer_port': port,
        'shared_files': []
    }

# Hàm khi peer chia sẻ file
def add_shared_file(peer_id, file_name):
    if peer_id in peerlist:
        peerlist[peer_id]['shared_files'].append(file_name)
        
    if file_name not in file_sharing:
        file_sharing[file_name] = []
    file_sharing[file_name].append(peer_id)


def get_peers_for_file(file_name):
    if file_name in file_sharing:
        print(file_sharing[file_name])
        return file_sharing[file_name]
    else:
        print("No peer have this file")
        return None





def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    try:
        while True:
            message = client_socket.recv(1024).decode("utf-8")
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
                print(metainfo)
                
                # respone peerlist to the client
                
                # response = f"Echo: {message}"
                # client_socket.send(response.encode("utf-8"))
            if data['action'] == 'fetch':
                pass
                                    
    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        print(f"Closing connection with {client_address}")
        client_socket.close()
    

def server(host, port):
    # handling server + multithread
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
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


if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    server(host, port)
