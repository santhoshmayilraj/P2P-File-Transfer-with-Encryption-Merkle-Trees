# **P2P File Transfer with Encryption & Merkle Trees**

Hi Again, This is Santhosh, your friendly neighbourhood coder. Alright, let’s do this one last time—this is **Secure P2P File Transfer**.

Welcome to this encrypted, integrity-verified file-sharing system! Here, we blend peer-to-peer networking, Caesar cipher encryption, and Merkle Trees to ensure your files are transferred securely and remain tamper-proof.

## 🔑 Key Features
- ✔ **Encrypted Chunks** – Files split & secured with Caesar cipher
- ✔ **Merkle Root Verification** – Ensures zero tampering during transfer
- ✔ **P2P Architecture** – Direct client-server file exchange
- ✔ **Lightweight & Fast** – Chunk-based processing for efficiency

## 🛠 How It Works

### 📤 Uploading a File (Client → Server)
1. Client sends a file (split into 10-byte chunks)
2. Server:
   - Encrypts each chunk (`caesar_encrypt`)
   - Generates SHA-256 hashes per chunk
   - Builds a Merkle Tree for integrity checks
   - Stores metadata (`filename_metadata.csv`, `chunk_metadata.csv`)

### 📥 Downloading a File (Server → Client)
1. Client requests a file
2. Server:
   - Verifies integrity using Merkle Root Hash
   - Decrypts chunks (`caesar_decrypt`)
   - Sends back the original file (if intact)

## 🔒 Encryption & Integrity

- **Caesar Cipher** – Shifts ASCII chars by +3 (encrypt) / -3 (decrypt)
- **Merkle Tree** – Detects any file corruption via root hash

## How to Run

### Steps

1. **Start the Server**
    ```bash
    python server.py
    ```

2. **Upload a File**
    ```bash
    python client.py
    ```

3. **Download a File**
    ```bash
    python client_request.py
    ```

## 📂 File Structure

```
├── client.py               # Uploads files to server  
├── client_request.py       # Requests file download  
├── server.py               # Handles uploads  
├── server_response.py      # Handles downloads  
├── caesar_encrypt.py       # Encrypts chunks  
├── caesar_decrypt.py       # Decrypts chunks  
├── merkel_tree.py          # Merkle Root Hash generator  
├── filename_metadata.csv   # File metadata storage  
└── chunk_metadata.csv      # Chunk hashes & encrypted data  
```

## 🌟 Why This Project?
- **End-to-end secure transfer** (Encryption + Integrity Check)
- **No middleman** – Direct P2P exchange
- **Lightweight & educational** – Great for learning encryption & hashing

Ready to share files securely?  **Let’s transfer!**