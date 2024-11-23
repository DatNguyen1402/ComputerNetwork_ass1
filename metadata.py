def split_file_into_pieces(file_path, piece_length):
    pieces_metadata = []
    with open(file_path, "rb") as file:
        file_size = 0  # Track file size
        while True:
            piece_data = file.read(piece_length)
            if not piece_data:
                break
            start_byte = file_size
            end_byte = file_size + len(piece_data) - 1
            pieces_metadata.append({
                "start_byte": start_byte,
                "end_byte": end_byte
            })
            file_size += len(piece_data)
    return pieces_metadata


def get_file_piece(file_path, start_byte, end_byte):
    with open(file_path, "rb") as file:
        file.seek(start_byte)
        return file.read(end_byte - start_byte + 1)

         # Separator for readability

def print_meta_data(pieces_metadata):
    for index, piece in enumerate(pieces_metadata):
        start_byte = piece["start_byte"]
        end_byte = piece["end_byte"]
        print(f"Piece {index + 1} (Bytes {start_byte} - {end_byte}):")
        
        
# Example usage:
file_path = "D:\HCMUT\HK241\ComputerNetwork\data\eBook.txt"
piece_length = 512*1024  # Define piece length (e.g., 600 bytes)

# Simulate splitting the file
pieces_metadata = split_file_into_pieces(file_path, piece_length)

# Print the data in the pieces
print_meta_data(pieces_metadata)


