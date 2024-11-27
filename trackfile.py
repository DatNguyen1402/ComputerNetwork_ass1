import os

def get_files_and_sizes(folder_path):
    # List to store file names and their sizes
    file_info = []
    
    # Check if the given path is a valid directory
    if not os.path.isdir(folder_path):
        print("The provided path is not a valid directory.")
        return
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if it's a file (ignore directories)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)  # Get the size of the file in bytes
            file_info.append((filename, file_size))
    
    # Print the result
    for file, size in file_info:
        print(f"File: {file}, Size: {size} bytes")
        
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

def check_file_share(file_name, file_share):
    for i in file_share: 
        if i == file_name:
            return 1 
    return 0 
