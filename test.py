def generate_request(num_pieces, peerlist):
    num_peers = len(peerlist)
    
    # Create a list of (peer_id, piece) pairs
    peer_requests = []

    for piece_index in range(0, num_pieces):
        # Select peer in a round-robin manner based on the piece index
        peer = peerlist[piece_index % num_peers]
        peer_id = peer['peer_id']
        peer_requests.append((peer_id, piece_index))

    return peer_requests

peerlist = [{'peer_id': 3, 'peerport': 4000},{'peer_id': 4, 'peerport': 4002}]

def get_peerport(peer_id, peerlist):
    for peer in peerlist:
        if peer['peer_id'] == peer_id:
            return peer['peerport']  
    return None 
if __name__ == "__main__":
    a = generate_request(8, peerlist)
    
    for peer_id, piece_index in a:
            peer_port = get_peerport(peer_id, peerlist)
            print(f"request piece{piece_index} form peer {peer_id} have port {peer_port}")
    print(a)