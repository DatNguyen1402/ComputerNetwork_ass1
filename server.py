import socket
import traceback  # For detailed error reporting
import threading

def handle_client(client_socket, client_address):
    # receive request from client
    
    # response 
    print(f"New connection from {client_address}")
    try:
        while True:
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break
            print(f"Received from {client_address}: {data}")
            response = f"Echo: {data}"
            client_socket.send(response.encode("utf-8"))
    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        print(f"Closing connection with {client_address}")
        client_socket.close()
    

def server():
    # handling server + multithread
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 65432))
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
    server()
