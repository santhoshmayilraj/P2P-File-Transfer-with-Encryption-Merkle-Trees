import socket
import threading
import os
import hashlib
import pandas as pd
import caesar_encrypt
import merkel_tree

Header = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

FILENAME_CSV_PATH = "filename_metadata.csv"
CHUNK_CSV_PATH = "chunk_metadata.csv"
filename_df = pd.DataFrame(columns=["filename", "roothash", "chunk_index", "chunk_hash"])
chunk_df = pd.DataFrame(columns=["chunk_hash", "encrypted_data"])

filename_df.to_csv(FILENAME_CSV_PATH, index=False)
chunk_df.to_csv(CHUNK_CSV_PATH, index=False)

def handle_client(conn, addr):
    global filename_df, chunk_df

    print(f"[NEW CONNECTION] {addr} connected.")

    try:
        filename_length = int(conn.recv(Header).decode(FORMAT).strip())
        filename = conn.recv(filename_length).decode(FORMAT)
        file_size = int(conn.recv(Header).decode(FORMAT).strip())

        file_data = b''
        with open(filename, 'wb') as file:
            chunk_index = 0
            while file_size > 0:
                data = conn.recv(min(file_size, 10))
                if not data:
                    break
                file.write(data)
                file.flush()
                os.fsync(file.fileno())
                file_size -= len(data)
                file_data += data
                chunk_hash = hashlib.sha256(data).hexdigest()
                encrypted_data = caesar_encrypt.caesar_encrypt(data)
                filename_df.loc[len(filename_df)] = [filename, "", chunk_index, chunk_hash]
                chunk_df.loc[len(filename_df)]=[chunk_hash,encrypted_data]
                chunk_index += 1
        root_hash = merkel_tree.calculate_merkle_root_whole_string(file_data,10)
        filename_df.loc[filename_df["filename"] == filename, "roothash"] = root_hash
        filename_df.to_csv(FILENAME_CSV_PATH, mode='a', header=False, index=False)
        chunk_df.to_csv(CHUNK_CSV_PATH, index=False)

        print(f"[MESSAGE] File '{filename}' received, saved, and metadata stored. Root hash: {root_hash}")

    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")

    finally:
        conn.close()
def start():
    server.listen()
    print(f"[LISTENING] Server listening on {SERVER}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[SERVER] Server started")
start()
