import socket
import threading
import os

SERVER_ADDRESS = '0.0.0.0' #the server address
SERVER_PORT = 8554
AUDIO_FILE = "song.wav"

# Buffer size for sending data
BUFFER_SIZE = 8192

def handle_client(client_socket):
    try:
        print("Client connected")

        # Read client requests
        request = client_socket.recv(BUFFER_SIZE).decode()
        print(f"Received request: {request}")

        if "PLAY" in request:
            with open(AUDIO_FILE, "rb") as audio_file:
                data = audio_file.read(BUFFER_SIZE)
                while data:
                    client_socket.sendall(data)
                    data = audio_file.read(BUFFER_SIZE)
        print("Finished streaming audio")
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()
        print("Client connection closed")

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server listening on {SERVER_ADDRESS}:{SERVER_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")

        # Handle the client in a new thread
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
