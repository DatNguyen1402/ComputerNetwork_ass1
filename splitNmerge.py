import os

def split_file_into_pieces(file_path, piece_length):
    pieces = []
    with open(file_path, "rb") as file:
        counter = 1
        while True:
            piece_data = file.read(piece_length)
            if not piece_data:
                break
            piece_file_path = f"{file_path}_piece{counter}"
            with open(piece_file_path, "wb") as piece_file:
                piece_file.write(piece_data)
            pieces.append(piece_file_path)
            counter += 1
    return pieces

def merge_pieces(piece_files, output_file_path):
    with open(output_file_path, "wb") as output_file:
        for piece_file in piece_files:
            with open(piece_file, "rb") as piece:
                output_file.write(piece.read())
    print(f"Merged {len(piece_files)} pieces into {output_file_path}")



