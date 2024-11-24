import os
import socket
import os
import threading
import math
from splitNmerge import split_file_into_pieces
from trackfile import get_files_and_sizes
from metainfo import split_file_into_pieces
from metainfo import get_file_piece
from metainfo import print_metainfo


# client 2 (peer2) 
host = 'localhost'
port = 5002
name = 'client 2'
file_dir = "../src/clients/client2/origin"
file_share = []

    
def check_file_path(file_path):
    print(f"Checking in the file path {file_path}")
    if not os.path.isdir(file_path):
        print("The provided path is not a valid directory.")
        return -1
    else:
        files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
        
        if files:
            print("Files in the directory:")
            for filename in files:
                print(filename)
            return 1  
        else:
            print("Directory is empty. No files found.")
            return 0

def check_file(file_path, file_name):
    print(f"Check if {file_name} in path {file_path}")
    flag = 0
    if not os.path.isdir(file_path):
        print("The provided path is not a valid directory.")
        return -1
    else:
        files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
        
        if files:
            for filename in files:
                if file_name == filename:
                    flag = 1    
    if flag == 0:
        print("File not found")
    if flag == 1:
        print("File found in path")
    return flag

def check_file_share(file_name):
    for i, metainfo in enumerate(file_share): 
        if metainfo['filename'] == file_name:
            print(f'File {file_name} found at index {i}.')
            return True 
    print(f'File {file_name} not found.')
    return False 




def generate_metainfo(file_name, file_path):
    files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
    metainfo = None

    if files:
        for filename in files:
            if file_name == filename:
                # Get the file size using os.path.getsize
                file_path = os.path.join(file_path, filename)
                filesize = os.path.getsize(file_path)
                
                # Calculate the number of pieces, rounding up if there's a remainder
                num_piece = math.ceil(filesize / (512 * 1024))
                
                metainfo = {
                    'filename': filename,
                    'filesize': filesize,
                    'num_piece': num_piece
                }
                
    return metainfo



def publish(file_name):
    print(f"Publish {file_name} to the network")
    if check_file(file_dir, file_name) == 1:
        if check_file_share(file_name) == 1:
            print("File have been there")
        else:
            # logic to update the file to network, need to update the metainfo?
            print(f"Pulish {file_name} successfully")
            # logic to make the metadata here
            metainfo = generate_metainfo(file_name, file_dir)
            file_share.append(metainfo)
    else:
        print("File not found in directory, cannot publish")
    



        
if __name__ == "__main__":

    publish('Chapter_3.pdf')
    publish('Chapter_3.pdf')
 
    #print_metainfo(split_file_into_pieces(f"{file_dir}/eBook.txt",500000))