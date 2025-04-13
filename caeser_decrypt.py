def caesar_decrypt(data):
    shift = 3
    decrypted_data = bytearray()

    for byte in data:
        if chr(byte).isalpha():  
            is_upper = chr(byte).isupper()
            decrypted_byte = byte - shift
            if is_upper:
                decrypted_byte = (decrypted_byte - ord('A')) % 26 + ord('A')
            else:
                decrypted_byte = (decrypted_byte - ord('a')) % 26 + ord('a')

            decrypted_data.append(decrypted_byte)
        else:
            decrypted_data.append(byte)

    return bytes(decrypted_data)

