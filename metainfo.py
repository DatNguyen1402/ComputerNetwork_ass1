import os
import hashlib
import json


def get_file_piece(file_path, start_byte, end_byte):
    with open(file_path, "rb") as file:
        file.seek(start_byte)
        return file.read(end_byte - start_byte + 1)



def split_file_into_pieces(file_name, piece_length):
    pieces = []
    file_size = os.path.getsize(file_name)
    
    with open(file_name, 'rb') as f:
        while True:
            piece = f.read(piece_length)
            if not piece:
                break
            sha1_hash = hashlib.sha1(piece).digest()  # SHA-1 hash của mỗi piece
            pieces.append(sha1_hash)
    
    return pieces, file_size

# Hàm tính toán SHA-1 hash cho từng piece
def calculate_piece_hash(piece):
    sha1 = hashlib.sha1()
    sha1.update(piece)
    return sha1.hexdigest()

def generate_metainfo(file_name, piece_length=512*1024):
    # Chia file thành các pieces và lấy danh sách hash SHA-1 của chúng
    pieces, file_size = split_file_into_pieces(file_name, piece_length)
    
    # Convert danh sách hash thành chuỗi duy nhất
    pieces_str = b''.join(pieces).hex()  # chuyển thành hex string
    
    metainfo = {
        "info": {
            "name": os.path.basename(file_name),  # Lấy tên file
            "piece length": piece_length,         # Chiều dài của mỗi piece (512KB)
            "pieces": pieces_str,                 # Chuỗi các SHA-1 hash
            "length": file_size                   # Kích thước file
        }
    }
    
    return metainfo

def read_metainfo(metainfo):
    info = metainfo['info']
    print(f"File name: {info['name']}")
    print(f"Piece length: {info['piece length']} bytes")
    print(f"File size: {info['length']} bytes")
    
    # Tính toán số pieces từ length
    num_pieces = len(info['pieces']) // 40  # 40 ký tự hex = 20 byte mỗi piece
    print(f"Number of pieces: {num_pieces}")

