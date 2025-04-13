def caesar_encrypt(data):
    shift = 3
    encrypted_data = bytearray()

    for byte in data:
        if chr(byte).isalpha():
            is_upper = chr(byte).isupper()
            encrypted_byte = byte + shift
            if is_upper:
                encrypted_byte = (encrypted_byte - ord('A')) % 26 + ord('A')
            else:
                encrypted_byte = (encrypted_byte - ord('a')) % 26 + ord('a')

            encrypted_data.append(encrypted_byte)
        else:
            encrypted_data.append(byte)

    return bytes(encrypted_data)