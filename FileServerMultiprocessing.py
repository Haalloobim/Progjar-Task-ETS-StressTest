from socket import *
import socket
import threading
import logging
import time
import sys
import os
from multiprocessing import Process, Queue, current_process
from concurrent.futures import ProcessPoolExecutor
import io

from FileProtocol import FileProtocol

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create an instance of FileProtocol for each process
def get_file_protocol():
    # Each process gets its own FileProtocol instance
    return FileProtocol()

# Global FileProtocol instance will be initialized in each process
fp = None

def init_worker():
    # This ensures each process gets its own FileProtocol instance
    global fp
    fp = get_file_protocol()
    pid = os.getpid()
    logging.info(f"Worker process {pid} initialized with new FileProtocol instance")

def ProcessTheClient(connection_info):
    """Handle a client connection in a separate process"""
    # Unpack the connection info
    client_socket_fd, client_address = connection_info
    
    # Recreate socket object from file descriptor
    connection = socket.fromfd(client_socket_fd, socket.AF_INET, socket.SOCK_STREAM)
    os.close(client_socket_fd)  # Close duplicate fd
    
    # Get process ID for logging
    pid = os.getpid()
    logging.info(f"Process {pid} handling client {client_address}")
    
    buffer = b''
    try:
        logging.info(f"Processing client {client_address} in process {pid}")
        connection.settimeout(300)  # 5-minute timeout
        
        while True:
            chunk = connection.recv(2**20)  # 1MB buffer size
            if not chunk:
                break
                
            buffer += chunk
            
            # Check if we have a complete message
            if b"\r\n\r\n" in buffer:
                # Get the complete message
                request = buffer.decode()
                logging.info(f"Complete request received from {client_address} ({len(buffer)} bytes) in process {pid}")
                
                # Process the request
                start_time = time.time()
                processed = fp.proses_string(request.strip())
                end_time = time.time()
                
                logging.info(f"Request processed in {end_time - start_time:.2f} seconds by process {pid}")
                
                # Send the response back
                response = processed + "\r\n\r\n"
                
                # Send in chunks for large responses
                response_bytes = response.encode()
                total_bytes = len(response_bytes)
                logging.info(f"Sending response ({total_bytes} bytes) from process {pid}")
                
                # Use a larger chunk size for sending
                chunk_size = 2**20  # 1MB chunks for sending
                for i in range(0, total_bytes, chunk_size):
                    connection.sendall(response_bytes[i:i+chunk_size])
                
                logging.info(f"Response sent to {client_address} from process {pid}")
                buffer = b''  # Reset buffer for next request
                
    except Exception as e:
        logging.error(f"Error handling client {client_address} in process {pid}: {e}")
    finally:
        logging.info(f"Closing connection with {client_address} from process {pid}")
        connection.close()

class Server:
    def __init__(self, ipaddress='0.0.0.0', port=6666, max_workers=10):
        self.ipinfo = (ipaddress, port)
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Set buffer sizes for better performance
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2**20)  # 1MB receive buffer
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2**20)  # 1MB send buffer
        self.max_workers = max_workers
        self.executor = None

    def run(self):
        logging.warning(f"Server running on {self.ipinfo} with ProcessPoolExecutor")
        self.my_socket.bind(self.ipinfo)
        self.my_socket.listen(10)
        
        # Create a process pool
        with ProcessPoolExecutor(max_workers=self.max_workers, initializer=init_worker) as self.executor:
            try:
                while True:
                    connection, address = self.my_socket.accept()
                    logging.warning(f"Accepted connection from {address}")
                    
                    # Get file descriptor to pass to child process
                    # This is key for multiprocessing - we pass the fd, not the socket object
                    connection_fd = connection.fileno()
                    connection_info = (connection_fd, address)
                    
                    # Submit the job to process pool
                    self.executor.submit(ProcessTheClient, connection_info)
                    
                    # Original connection is duplicated in the child process, so we close it here
                    connection.close()
                    
            except KeyboardInterrupt:
                logging.warning("Server shutting down.")
            finally:
                logging.warning("Closing server socket")
                self.my_socket.close()


def main():
    # Adjust the number of workers based on your CPU cores
    # For CPU-bound tasks, it's common to use N = number of CPU cores
    import multiprocessing
    cpu_count = multiprocessing.cpu_count()
    optimal_workers = max(2, cpu_count)  # At least 2, but ideally match CPU count
    
    logging.info(f"System has {cpu_count} CPU cores, using {optimal_workers} worker processes")
    
    svr = Server(ipaddress='0.0.0.0', port=6666, max_workers=optimal_workers)
    svr.run()


if __name__ == "__main__":
    main()