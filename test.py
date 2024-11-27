import os

file_dir = "../src/clients/client2/origin"

def send_piece_to_client(file_name, piece_index, piece_size=512*1024):
    file_path = os.path.join(file_dir, file_name)
    
    try:
        with open(file_path, 'rb') as f:
            # Move the file pointer to the start of the requested piece
            f.seek(piece_index * piece_size)
            # Read the specified piece
            data = f.read(piece_size)
        
        if not data:
            print(f"No data found for piece {piece_index} of file {file_name}")
            return
        
        offset = 0
        chunk_size = 4096
        while offset < len(data):
            chunk = data[offset:offset + chunk_size]
            print(chunk)
            offset += chunk_size
                
    except FileNotFoundError:
        print(f"File {file_name} not found.")
    except Exception as e:
        print(f"Error while sending piece: {e}")

if __name__ == "__main__":
    send_piece_to_client('eBook.txt', 0)
