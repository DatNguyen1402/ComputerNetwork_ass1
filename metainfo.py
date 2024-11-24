def split_file_into_pieces(file_path, piece_length):
    pieces_metainfo = []
    with open(file_path, "rb") as file:
        file_size = 0  # Track file size
        while True:
            piece_data = file.read(piece_length)
            if not piece_data:
                break
            start_byte = file_size
            end_byte = file_size + len(piece_data) - 1
            pieces_metainfo.append({
                "start_byte": start_byte,
                "end_byte": end_byte
            })
            file_size += len(piece_data)
    return pieces_metainfo


def get_file_piece(file_path, start_byte, end_byte):
    with open(file_path, "rb") as file:
        file.seek(start_byte)
        return file.read(end_byte - start_byte + 1)

def print_metainfo(pieces_metainfo):
    for index, piece in enumerate(pieces_metainfo):
        start_byte = piece["start_byte"]
        end_byte = piece["end_byte"]
        print(f"Piece {index + 1} (Bytes {start_byte} - {end_byte}):")


