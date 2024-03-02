def xor_cipher(text, key):
    """
    Encrypts the text using the XOR cipher with the given key.
    """
    # convert the text to binary
    binary_text = []
    for char in text:
        binary_text.append(format(ord(char), '08b'))

    # convert the key to binary
    binary_key = "".join(format(ord(key), '08b'))

    cipher = "" 
    for b in binary_text:
        # XOR operation
        text_xor_key = [str(int(b[i]) ^ int(binary_key[i])) for i in range(8)]
        # convert the result to a character and add it to the cipher
        cipher += chr(int("".join(text_xor_key), 2))

    return cipher
