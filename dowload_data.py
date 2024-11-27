import socket
import os
import json

def generate_request(num_pieces, peerlist):
    num_peers = len(peerlist)
    
    peer_requests = []

    for piece_index in range(num_pieces):
        peer = peerlist[piece_index % num_peers]
        peer_id = peer['peer_id']
        peer_requests.append((peer_id, piece_index))

    return peer_requests

def handle_file_request(sock_peer_peer, file_dir):
    try:
        data = sock_peer_peer.recv(4096).decode()
        # message = json.loads(data)
        if data:
            print(f"client2 get {data}")
        message = json.loads(data)
        if message['action'] == 'send_file':
            file_name = message['file_name']
            piece_index = message['piece_index']
            send_piece_to_client(sock_peer_peer, file_dir, file_name, piece_index)
    finally:
        sock_peer_peer.close()

def request_piece(file_dir, file_name, piece_index, peer_port, peer_ip):
    try:
        print("Trying to connect 1")
        sock_peer_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        filepath = os.path.join(file_dir, file_name)
        sock_peer_peer.connect((peer_ip, peer_port))
        sock_peer_peer.sendall(json.dumps({
            'action': 'send_file', 
            'file_name': file_name, 
            'piece_index': piece_index
        }).encode() + b'\n')

        with open(f"{filepath}_piece{piece_index}", 'wb') as f:
            while True:
                data = sock_peer_peer.recv(4096)
                if not data:
                    break
                f.write(data)

        print(f"Downloaded piece {piece_index} of {file_name}")
    except Exception as e:
        print(f"Error downloading piece {piece_index}: {e}")
    finally:
        sock_peer_peer.close()


def send_piece_to_client(sock_peer_peer, file_dir, file_name, piece_index, piece_size=512*1024):
    file_path = os.path.join(file_dir, file_name)
    try:
        with open(file_path, 'rb') as f:

            f.seek(piece_index * piece_size)
            data = f.read(piece_size)
        
        offset = 0
        chunk_size = 4096
        while offset < len(data):
            chunk = data[offset:offset + chunk_size]
            sock_peer_peer.sendall(chunk)
            offset += chunk_size
                
    except FileNotFoundError:
        print(f"File {file_name} not found.")
    except Exception as e:
        print(f"Error while sending piece: {e}")
        

def merge_pieces(filedir, file_name, total_pieces):
    filepath = os.path.join(filedir, file_name)
    with open(filepath, 'wb') as merged_file:
        for piece_index in range(total_pieces):
            piece_filename = f"{filepath}_piece{piece_index}"
            
            if os.path.exists(piece_filename):
                # Read each piece in binary mode and write it to the merged file
                with open(piece_filename, 'rb') as piece_file:
                    merged_file.write(piece_file.read())
                os.remove(piece_filename)  # can be remove
            else:
                print(f"Warning: Piece {piece_filename} does not exist.")
    
    print(f"Merging complete: {filepath}")