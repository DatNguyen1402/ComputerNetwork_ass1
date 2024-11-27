import os

file_dir = "../src/clients/client1/origin"

def merge_pieces(filedir, file_name, total_pieces):
    filepath = os.path.join(filedir, file_name)
    with open(filepath, 'wb') as merged_file:
        for piece_index in range(total_pieces):
            piece_filename = f"{filepath}_piece{piece_index}"
            
            if os.path.exists(piece_filename):
                # Read each piece in binary mode and write it to the merged file
                with open(piece_filename, 'rb') as piece_file:
                    merged_file.write(piece_file.read())
                os.remove(piece_filename)
            else:
                print(f"Warning: Piece {piece_filename} does not exist.")
    
    print(f"Merging complete: {filepath}")

if __name__ == "__main__":
    merge_pieces(file_dir, 'eBook.txt', 7)
