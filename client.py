import os
import socket


class client:
    def __init__(self, host, port, ):
        self.host = host
        self.port = port
        self.socket = None


    def fetch(self,file_name):
        # connect to the the server
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket.connect((host, port))
        request = f"find {file_name}"
        self.socket.send(request.encode("utf-8"))
        response = self.socket.recv(1024).decode('utf-8')
        print(f"Server response : {response}")
        
if __name__ == "__main__":
    host = 'localhost'
    port = 50000
    client1 = client('localhost', 50000)
    client1.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client1.socket.connect((host, port))
        client1.fetch('data.txt')
    except Exception as e:
        print(f"Connection error: {e}")    
        
    finally:
        client1.socket.close()
        print("Client connection closed")    
        
    