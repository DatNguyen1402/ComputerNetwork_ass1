import os

def get_files_and_sizes(folder_path):
    # List to store file names and their sizes
    file_info = []
    
    # Check if the given path is a valid directory
    if not os.path.isdir(folder_path):
        print("The provided path is not a valid directory.")
        return
    
    # Iterate over the files in the given folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Check if it's a file (ignore directories)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)  # Get the size of the file in bytes
            file_info.append((filename, file_size))
    
    # Print the result
    for file, size in file_info:
        print(f"File: {file}, Size: {size} bytes")
        
        


if __name__ == "__main__":
    folder_path = "D:\HCMUT\HK241\Computer Architecture slide\Lab\Assignment"  # Replace with your folder path
    get_files_and_sizes(folder_path)
