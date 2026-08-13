# P2P File Transfer with Encryption & Merkle Trees

A peer-to-peer file transfer project exploring chunk-based file transmission, basic encryption, hashing, and Merkle tree-based integrity verification.

The project splits files into chunks, processes them before transfer, and uses a Merkle tree to verify whether the transferred data has been modified or corrupted.

## Overview

The system consists of a client and server that communicate to transfer files in chunks.

The main concepts explored are:

- Peer-to-peer file transfer
- Chunk-based file processing
- Caesar cipher encryption
- SHA-256 hashing
- Merkle trees
- File integrity verification
- Client-server communication

## How It Works

### Upload

```text
File
 │
 ▼
Split into Chunks
 │
 ▼
Encrypt Chunks
 │
 ▼
SHA-256 Hashes
 │
 ▼
Build Merkle Tree
 │
 ▼
Transfer & Store
```

The client divides the file into 10-byte chunks. The chunks are encrypted before being processed and transferred.

SHA-256 hashes are generated for the chunks and used to construct a Merkle tree. The resulting Merkle root represents the integrity state of the file.

Download
```text
Stored Chunks
 │
 ▼
Request File
 │
 ▼
Verify Integrity
 │
 ▼
Decrypt Chunks
 │
 ▼
Reconstruct File
```

During retrieval, the stored data is checked against the Merkle root before the encrypted chunks are decrypted and reconstructed into the original file.

Encryption & Integrity
Caesar Cipher

The project uses a Caesar cipher that shifts ASCII characters by a fixed offset:

Encryption:  +3
Decryption:  -3

This is implemented as a learning exercise and is not considered secure cryptography for real-world file protection.

Merkle Tree

SHA-256 hashes are generated for individual chunks and combined recursively to produce a Merkle root.

             Root
            /    \
          H12    H34
         /  \   /  \
       H1   H2 H3   H4
       │    │  │    │
      C1   C2 C3   C4

The root hash can be used to detect changes or corruption within the transferred data.

```text
File Structure
├── client.py               # Handles file uploads
├── client_request.py       # Requests file downloads
├── server.py               # Handles incoming uploads
├── server_response.py      # Handles file responses
├── caesar_encrypt.py       # Encrypts file chunks
├── caesar_decrypt.py       # Decrypts file chunks
├── merkel_tree.py          # Generates Merkle tree hashes
├── filename_metadata.csv   # File metadata
└── chunk_metadata.csv      # Chunk and hash metadata
```
Running the Project
Start the Server
python server.py
Upload a File
python client.py
Request a File
python client_request.py
What I Explored

This project was built to understand how several fundamental concepts in computer systems and security fit together:

Network-based file transfer
Chunking and file reconstruction
Symmetric transformation of data
Cryptographic hashing
Merkle trees
Data integrity verification
Client-server communication

The project focuses on understanding the underlying mechanisms rather than providing production-grade file security.
