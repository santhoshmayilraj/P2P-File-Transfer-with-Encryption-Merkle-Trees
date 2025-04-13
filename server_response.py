import socket
import threading
import pandas as pd
import hashlib
import caeser_decrypt

Header = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
def calculate_merkle_root(file_chunks):
    if not file_chunks:
        return hashlib.sha256(b'').hexdigest()

    while len(file_chunks) > 1:
        new_chunks = []

        for i in range(0, len(file_chunks), 2):
            chunk1 = file_chunks[i]

            if i + 1 < len(file_chunks):
                chunk2 = file_chunks[i + 1]
            else:
                chunk2 = chunk1
            combined = chunk1.encode('utf-8') + chunk2.encode('utf-8')
            new_hash = hashlib.sha256(combined).hexdigest()
            new_chunks.append(new_hash)

        file_chunks = new_chunks

    return file_chunks[0]
def verify_integrity(file_name, root_hash, chunk_hashes):
    calculated_root_hash = calculate_merkle_root(chunk_hashes)
    return root_hash == calculated_root_hash

def get_file_data(file_name, chunk_hashes, chunk_data_df):
    file_data = b""
    for chunk_hash in chunk_hashes:
        chunk_data = chunk_data_df.loc[chunk_data_df['chunk_hash'] == chunk_hash, 'encrypted_data'].values[0]
        chunk_data_bytes = chunk_data.encode('utf-8')
        file_data = file_data + chunk_data_bytes
    return file_data
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    try:
        filename = conn.recv(Header).decode(FORMAT).strip()
        file_metadata_df = pd.read_csv("filename_metadata.csv")
        chunk_metadata_df = pd.read_csv("chunk_metadata.csv")
        file_info = file_metadata_df.loc[file_metadata_df['filename'] == filename].iloc[0]
        file_info_new = file_metadata_df.loc[file_metadata_df['filename'] == filename]
        root_hash = file_info['roothash']
        chunk_hashes = list(file_info_new['chunk_hash'])

        if verify_integrity(filename, root_hash, chunk_hashes):
            print(f"File integrity maintained for {filename}")
            file_data = get_file_data(filename, chunk_hashes, chunk_metadata_df)
            decrypted_data = caeser_decrypt.caesar_decrypt(file_data)
            conn.send(f"{len(file_data):<{Header}}".encode(FORMAT))
            conn.send(decrypted_data)
        else:
            print(f"Data is corrupted for {filename}. Integrity not maintained.")
            conn.send("0".encode(FORMAT))
            conn.send("File is corrupted. Integrity not maintained.".encode(FORMAT))
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
    finally:
        conn.close()
        print(f"[CONNECTION CLOSED] {addr} connection closed.")

def start():
    server.listen()
    print(f"[LISTENING] Server listening on {SERVER}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    print("[SERVER] Server started")
    start()
