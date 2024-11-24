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
        
        #maybe should response the peer have the file with the peer info and the file info(the num of piece to start handle)
        response = self.socket.recv(1024).decode('utf-8')
        
        # start dowload use the peer list and piece list
        # create thread for each peer to download
        # maybe note the flag ? to decide the piece have downloaded
        
        # send request to the peer 
        
        # recieve the response (the data of piece)
        
        
        print(f"Server response : {response}")





    
    def publish(self,file_name):
        command ={
            'action' : 'publish'
        }
        
        request = f"publish {file_name}"
        self.socket.send(request.encode("utf-8"))
        response = self.socket.recv(1024).decode('utf-8')
        print(f"Server response : {response}")
    
    def connect_to_peer(self, host, port):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            print(f"host({self.host}) connect to host:{host} and port:{port}")
            request = "dowload"
            self.socket.send(request.encode())
            response = self.socket.recv(1024).decode()
            print(f"recive response :{response}")
        except Exception as e:
            print(f"Connection failed: {e}")   
        finally:
            self.socket.close()  
            
    def response_to_peer(self):
        try:
            # Create a socket to listen for incoming connections
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)  # Listen for incoming connections
            print(f"Listening for connections on {self.host}:{self.port}...")

            while True:
                # Accept a connection from a peer
                client_socket, addr = self.socket.accept()
                print(f"Connected by {addr}")

                # Receive a request from the connected peer
                request = client_socket.recv(1024).decode()
                print(f"Received request: {request}")

                # Process the request (in this case, we handle a "download" request)
                if request == "download":
                    # Send a response (this could be the file content or a message)
                    response = "Here is the file content"  # Example response
                    client_socket.send(response.encode())
                    print(f"Sent response: {response}")

                client_socket.close()  # Close the connection to this peer

        except Exception as e:
            print(f"Error in response handling: {e}")
        finally:
            self.socket.close()  # Ensure the socket is closed after use
        
        
if __name__ == "__main__":

    
    client2 = client('localhost', 5002)


    client2.response_to_peer()

