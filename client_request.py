import socket
import os

Header = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
def request_file(filename):
    client.send(f"{filename:<{Header}}".encode(FORMAT))
    file_size = int(client.recv(Header).decode(FORMAT).strip())
    if file_size:
        file_data = client.recv(file_size)
        with open(filename, 'wb') as file:
            file.write(file_data)
        print(f"Received and saved {filename} from server.")
        os.startfile(filename)
    else:
        print(f"File {filename} not found on server or is insecure")
filename_to_request = "test_1.txt"
request_file(filename_to_request)
client.close()
