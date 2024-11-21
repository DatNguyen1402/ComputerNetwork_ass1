import os
import socket

def client(host='localhost', port=65432):
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket. connect((host, port))
        message = "Hello, Socket Server!"
        client_socket.send(message.encode("utf-8"))
        response = client_socket.recv(1024).decode('utf-8')
        
        print(f"Server response : {response}")
        
    except Exception as e:
        print(f"Connection error: {e}")
    
    finally:
        client_socket.close()
        print("Client connection closed")

if __name__ == "__main__":
    client()
