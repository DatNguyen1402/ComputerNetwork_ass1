peerlist = {}  
file_sharing = {}  
file_metadata ={}


def add_peer(peer_id, peer_name, peer_ip, port):
    peerlist[peer_id] = {
        'peer_name': peer_name,
        'peer_port': port,
        'peer_ip': peer_ip,
        'shared_files': []
    }

def add_shared_file(peer_id, file_name, metainfo):
    if file_name in peerlist[peer_id]['shared_files']:
        return

    # Add the file to the peer's shared files list
    peerlist[peer_id]['shared_files'].append(file_name)

    # Add the peer to the file_sharing dict for the given file
    if file_name not in file_sharing:
        file_sharing[file_name] = []
    file_sharing[file_name].append(peer_id)

    # Add the file metadata to the file_metadata dictionary
    if file_name not in file_metadata:
        file_metadata[file_name] = metainfo

    return 1

def get_peers_for_file(file_name):
    peers_have_file = []
    
    if file_name in file_sharing:
        peer_ids = file_sharing[file_name]
        
        for peer_id in peer_ids:
            if peer_id in peerlist:
                peer_info = {
                    'peer_id': peer_id,
                    'peer_name': peerlist[peer_id]['peer_name'],
                    'peer_ip' : peerlist[peer_id]['peer_ip'],
                    'peer_port': peerlist[peer_id]['peer_port'],
                }
                peers_have_file.append(peer_info)
    
    return peers_have_file

def remove_peer(peer_id):
    if peer_id in peerlist:
        
        peer_name = peerlist[peer_id]['peer_name']
        print(f"Removing peer {peer_name} (ID: {peer_id}) from the network")
        
        del peerlist[peer_id]

        files_to_remove = []
        for file_name, peers in file_sharing.items():
            if peer_id in peers:
                peers.remove(peer_id)

                if not peers:
                    files_to_remove.append(file_name)

        for file_name in files_to_remove:
            del file_sharing[file_name]

        print(f"Peer {peer_name} and shared files removed successfully")

def get_peerport(peer_id, peerlist):
    for peer in peerlist:
        if peer['peer_id'] == peer_id:
            return peer['peer_port']  
    return None  

def get_peerip(peer_id, peerlist):
    for peer in peerlist:
        if peer['peer_id'] == peer_id:
            return peer['peer_ip']  
    return None  

def getmetainfo(file_name, file_metadata):
    return file_metadata[file_name]