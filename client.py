import socket
import os

Header = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
def send_file(filename):
    try:
        filename_length = len(filename)
        client.sendall(f"{filename_length:<{Header}}".encode(FORMAT))
        client.sendall(filename.encode(FORMAT))
        file_size = os.path.getsize(filename)
        client.sendall(f"{file_size:<{Header}}".encode(FORMAT))
        with open(filename, 'rb') as file:
            while True:
                data = file.read(10)
                if not data:
                    break
                client.sendall(data)

        print("File has been sent!")

    except Exception as e:
        print(f"Error sending file: {e}")
send_file(r"test_1.txt")
client.close()
