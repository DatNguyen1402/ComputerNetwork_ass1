import os
import hashlib
import bencodepy

def generate_piece_hashes(file_path, piece_size):
    """Generate SHA-1 hashes for each piece of the file."""
    hashes = []
    with open(file_path, 'rb') as f:
        while chunk := f.read(piece_size):
            hash_obj = hashlib.sha1(chunk)
            hashes.append(hash_obj.digest())  # SHA-1 hash of the chunk
    return hashes

def create_torrent_file(input_path, tracker_url, piece_size, output_torrent_path):
    """Create a torrent file for the given input file or folder."""
    torrent_data = {
        "announce": tracker_url,  # Tracker URL
        "info": {}
    }
    
    # Handle single file
    if os.path.isfile(input_path):
        file_name = os.path.basename(input_path)
        file_size = os.path.getsize(input_path)
        
        # Generate piece hashes
        piece_hashes = generate_piece_hashes(input_path, piece_size)
        
        # Add metadata to the torrent
        torrent_data["info"] = {
            "name": file_name,
            "length": file_size,
            "piece length": piece_size,
            "pieces": b"".join(piece_hashes),  # Concatenate hashes
        }
    else:
        # Multi-file handling (folder)
        raise NotImplementedError("Multi-file torrents are not implemented in this example.")
    
    # Encode the torrent data using bencode
    encoded_torrent = bencodepy.encode(torrent_data)
    
    # Save the .torrent file
    with open(output_torrent_path, "wb") as torrent_file:
        torrent_file.write(encoded_torrent)
    
    print(f"Torrent file created at {output_torrent_path}")

# Example usage
if __name__ == "__main__":
    input_file = "example_file.txt"  # File you want to share
    tracker = "http://example-tracker.com/announce"  # Replace with actual tracker URL
    piece_size = 256 * 1024  # 256 KB piece size
    output_torrent = "example_file.torrent"
    
    create_torrent_file(input_file, tracker, piece_size, output_torrent)
