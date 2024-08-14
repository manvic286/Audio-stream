import socket
import pyaudio

SERVER_ADDRESS = 'localhost' #the server ip address
SERVER_PORT = 8554
BUFFER_SIZE = 8192

# Audio configuration
AUDIO_FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

def play_audio(data_stream):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=AUDIO_FORMAT, channels=CHANNELS, rate=RATE, output=True)
    
    try:
        while True:
            data = data_stream.recv(BUFFER_SIZE)
            if not data:
                break
            stream.write(data)
    except Exception as e:
        print(f"Error playing audio: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

    try:
        # Send a request to play the audio stream
        client_socket.sendall(b"PLAY")

        # Start receiving and playing audio
        play_audio(client_socket)
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
