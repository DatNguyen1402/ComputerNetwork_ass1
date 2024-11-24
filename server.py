import socket
import traceback  # For detailed error reporting
import threading

peer_list = []

class PeerInfo:
    def __init__(self, name):
        self.name = name
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







def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    try:
        while True:
            request = client_socket.recv(1024).decode("utf-8")
            if not request:
                break
            print(f"Received from {client_address}: {request}")
            
            #response
            response = f"Echo: {request}"
            client_socket.send(response.encode("utf-8"))
                                    
    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        print(f"Closing connection with {client_address}")
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


if __name__ == "__main__":
    # host = '0.0.0.0'
    # port = 50000
    # server(host, port)
    peer1 = PeerInfo('peer1')
    peer2 = PeerInfo('peer2')
    peer_list.append(peer1)
    add_or_update_peer('peer3','data.txt')
    peer_list.append(peer2)
    show_peers()