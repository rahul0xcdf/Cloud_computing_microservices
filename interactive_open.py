# fixed_interactive_open.py - Interactive implementation of open() system call with improved error handling
import os
import errno
import traceback
from enum import Enum, auto

class FileMode(Enum):
    READ = auto()      # r
    WRITE = auto()     # w
    APPEND = auto()    # a
    READ_PLUS = auto() # r+
    WRITE_PLUS = auto() # w+
    APPEND_PLUS = auto() # a+

class FileDescriptor:
    def __init__(self, path, mode, file_obj=None):
        self.path = path
        self.mode = mode
        self.file_obj = file_obj
        self.position = 0
        self.is_open = True

class FileDescriptorTable:
    def __init__(self):
        self.fd_table = {}
        self.next_fd = 3  # Start after stdin, stdout, stderr

    def add_file(self, path, mode, file_obj):
        fd = self.next_fd
        self.fd_table[fd] = FileDescriptor(path, mode, file_obj)
        self.next_fd += 1
        return fd

    def get_file(self, fd):
        if fd not in self.fd_table:
            raise OSError(errno.EBADF, "Bad file descriptor")
        return self.fd_table[fd]

    def close_file(self, fd):
        if fd not in self.fd_table:
            raise OSError(errno.EBADF, "Bad file descriptor")
        descriptor = self.fd_table[fd]
        if descriptor.file_obj:
            descriptor.file_obj.close()
        descriptor.is_open = False
        del self.fd_table[fd]
    
    def list_open_files(self):
        return [(fd, descriptor.path, descriptor.mode) for fd, descriptor in self.fd_table.items()]

# Global file descriptor table
fd_table = FileDescriptorTable()

def custom_open(path, flags="r"):
    """
    Implementation of the open() system call.
    
    Args:
        path: Path to the file to open
        flags: File mode flags (r, w, a, r+, w+, a+)
    
    Returns:
        A file descriptor (integer)
    """
    # Map string flags to our enum
    mode_map = {
        "r": FileMode.READ,
        "w": FileMode.WRITE,
        "a": FileMode.APPEND,
        "r+": FileMode.READ_PLUS,
        "w+": FileMode.WRITE_PLUS,
        "a+": FileMode.APPEND_PLUS
    }
    
    if flags not in mode_map:
        raise ValueError(f"Invalid file mode: {flags}")
    
    mode = mode_map[flags]
    
    try:
        # Print debug info
        print(f"Trying to open file: {path} with mode: {flags}")
        
        # Get absolute path for clarity
        abs_path = os.path.abspath(path)
        print(f"Absolute path: {abs_path}")
        
        # Map our enum back to Python's file mode strings
        python_mode = flags
        file_obj = open(abs_path, python_mode)
        
        print(f"File successfully opened using Python's built-in open()")
        
        fd = fd_table.add_file(abs_path, mode, file_obj)
        return fd
    except IOError as e:
        print(f"IOError: {e.strerror} (errno: {e.errno})")
        
        # Check if directory exists
        dir_path = os.path.dirname(abs_path) or '.'
        if not os.path.exists(dir_path):
            print(f"Directory does not exist: {dir_path}")
        
        # Check write permissions
        if not os.access(dir_path, os.W_OK):
            print(f"No write permission in directory: {dir_path}")
            
        raise OSError(e.errno, f"Cannot open file {path}: {e.strerror}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        traceback.print_exc()
        raise

def custom_read(fd, size):
    """
    Read from an open file descriptor.
    
    Args:
        fd: File descriptor
        size: Number of bytes to read
    
    Returns:
        Data read from the file
    """
    descriptor = fd_table.get_file(fd)
    
    if not descriptor.is_open:
        raise OSError(errno.EBADF, "File descriptor is closed")
    
    if descriptor.mode not in [FileMode.READ, FileMode.READ_PLUS, 
                               FileMode.WRITE_PLUS, FileMode.APPEND_PLUS]:
        raise OSError(errno.EACCES, "File not opened for reading")
    
    try:
        data = descriptor.file_obj.read(size)
        descriptor.position += len(data)
        return data
    except IOError as e:
        raise OSError(e.errno, f"Error reading from file: {e.strerror}")

def custom_write(fd, data):
    """
    Write to an open file descriptor.
    
    Args:
        fd: File descriptor
        data: Data to write
    
    Returns:
        Number of bytes written
    """
    descriptor = fd_table.get_file(fd)
    
    if not descriptor.is_open:
        raise OSError(errno.EBADF, "File descriptor is closed")
    
    if descriptor.mode not in [FileMode.WRITE, FileMode.APPEND, 
                               FileMode.READ_PLUS, FileMode.WRITE_PLUS, 
                               FileMode.APPEND_PLUS]:
        raise OSError(errno.EACCES, "File not opened for writing")
    
    try:
        descriptor.file_obj.write(data)
        bytes_written = len(data)
        descriptor.position += bytes_written
        return bytes_written
    except IOError as e:
        raise OSError(e.errno, f"Error writing to file: {e.strerror}")

def custom_close(fd):
    """
    Close a file descriptor.
    
    Args:
        fd: File descriptor to close
    """
    fd_table.close_file(fd)

def custom_lseek(fd, offset, whence):
    """
    Reposition the file offset of the open file descriptor.
    
    Args:
        fd: File descriptor
        offset: Offset in bytes
        whence: 0 (SEEK_SET), 1 (SEEK_CUR), or 2 (SEEK_END)
    
    Returns:
        The resulting offset position
    """
    descriptor = fd_table.get_file(fd)
    
    if not descriptor.is_open:
        raise OSError(errno.EBADF, "File descriptor is closed")
    
    try:
        # Map whence values to Python's constants
        whence_map = {
            0: os.SEEK_SET,  # SEEK_SET
            1: os.SEEK_CUR,  # SEEK_CUR
            2: os.SEEK_END   # SEEK_END
        }
        
        if whence not in whence_map:
            raise ValueError(f"Invalid whence value: {whence}")
        
        new_position = descriptor.file_obj.seek(offset, whence_map[whence])
        descriptor.position = new_position
        return new_position
    except IOError as e:
        raise OSError(e.errno, f"Error seeking in file: {e.strerror}")

def display_environment_info():
    """Display helpful environment information for debugging"""
    print("\n----- ENVIRONMENT INFO -----")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Temp directory: {os.path.abspath(os.path.join(os.getcwd(), 'temp'))}")
    try:
        os.makedirs("temp", exist_ok=True)
        print("Successfully created temp directory")
    except Exception as e:
        print(f"Could not create temp directory: {e}")
    print("----------------------------\n")

def interactive_demo():
    """Interactive demonstration of custom open system call"""
    print("=" * 60)
    print("CUSTOM OPEN() SYSTEM CALL IMPLEMENTATION DEMO")
    print("=" * 60)
    
    display_environment_info()
    
    while True:
        print("\nAvailable operations:")
        print("1. Create a new file")
        print("2. Open an existing file")
        print("3. Write to a file")
        print("4. Read from a file")
        print("5. Close a file")
        print("6. Delete a file")
        print("7. List open files")
        print("8. Exit")
        
        choice = input("\nSelect an operation (1-8): ")
        
        if choice == "1":
            filename = input("Enter filename to create (e.g., temp/test.txt): ")
            try:
                fd = custom_open(filename, "w")
                print(f"File created successfully! File descriptor: {fd}")
            except Exception as e:
                print(f"Error creating file: {e}")
        
        elif choice == "2":
            filename = input("Enter filename to open: ")
            mode = input("Enter mode (r, w, a, r+, w+, a+): ")
            try:
                fd = custom_open(filename, mode)
                print(f"File opened successfully! File descriptor: {fd}")
            except Exception as e:
                print(f"Error opening file: {e}")
        
        elif choice == "3":
            try:
                fd = int(input("Enter file descriptor: "))
                text = input("Enter text to write: ")
                bytes_written = custom_write(fd, text + "\n")
                print(f"Successfully wrote {bytes_written} bytes to file.")
            except Exception as e:
                print(f"Error writing to file: {e}")
        
        elif choice == "4":
            try:
                fd = int(input("Enter file descriptor: "))
                size_str = input("Enter number of bytes to read (press Enter for all): ")
                size = int(size_str) if size_str.strip() else 1024
                content = custom_read(fd, size)
                print("\n----- FILE CONTENT -----")
                print(content, end="")
                print("-----------------------")
            except Exception as e:
                print(f"Error reading file: {e}")
        
        elif choice == "5":
            try:
                fd = int(input("Enter file descriptor to close: "))
                custom_close(fd)
                print(f"File descriptor {fd} closed successfully.")
            except Exception as e:
                print(f"Error closing file: {e}")
        
        elif choice == "6":
            filename = input("Enter filename to delete: ")
            try:
                os.remove(filename)
                print(f"File {filename} deleted successfully.")
            except Exception as e:
                print(f"Error deleting file: {e}")
        
        elif choice == "7":
            print("\n----- OPEN FILES -----")
            open_files = fd_table.list_open_files()
            if open_files:
                for fd, path, mode in open_files:
                    print(f"FD: {fd}, Path: {path}, Mode: {mode}")
            else:
                print("No open files.")
            print("-----------------------")
        
        elif choice == "8":
            print("Exiting demo. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please select a number from 1-8.")

if __name__ == "__main__":
    interactive_demo()