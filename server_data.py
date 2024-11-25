peerlist = {}  
file_sharing = {}  

def add_peer(peer_id, peer_name, port):
    peerlist[peer_id] = {
        'peer_name': peer_name,
        'peer_port': port,
        'shared_files': []
    }


def add_shared_file(peer_id, file_name):
    if file_name in peerlist[peer_id]['shared_files']:
        return

    peerlist[peer_id]['shared_files'].append(file_name)

    if file_name not in file_sharing:
        file_sharing[file_name] = []
    
    file_sharing[file_name].append(peer_id)
    return 1

def get_peers_for_file(file_name):
    peers_have_file = []
    
    # Kiểm tra file có trong file_sharing hay không
    if file_name in file_sharing:
        peer_ids = file_sharing[file_name]
        
        # Lấy thông tin chi tiết của từng peer dựa trên peer_id
        for peer_id in peer_ids:
            if peer_id in peerlist:
                peer_info = {
                    'peer_id': peer_id,
                    'peer_name': peerlist[peer_id]['peer_name'],
                    'peer_port': peerlist[peer_id]['peer_port']
                }
                peers_have_file.append(peer_info)
    
    return peers_have_file

def remove_peer(peer_id):
    if peer_id in peerlist:
        # Lấy tên peer và xóa khỏi danh sách peerlist
        peer_name = peerlist[peer_id]['peer_name']
        print(f"Removing peer {peer_name} (ID: {peer_id}) from the network")

        # Xóa peer khỏi peerlist
        del peerlist[peer_id]

        # Xóa peer khỏi danh sách file_sharing cho các file mà peer này đã chia sẻ
        files_to_remove = []
        for file_name, peers in file_sharing.items():
            if peer_id in peers:
                peers.remove(peer_id)
                # Nếu không còn peer nào chia sẻ file này, xóa file khỏi file_sharing
                if not peers:
                    files_to_remove.append(file_name)

        for file_name in files_to_remove:
            del file_sharing[file_name]

        print(f"Peer {peer_name} and shared files removed successfully")

