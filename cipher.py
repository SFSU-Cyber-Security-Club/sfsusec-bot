import random
import base64

async def generate_key():
    '''
    Generates a random 5 letter/digit key
    '''
    key = "".join((chr(random.randint(48, 57))if random.choice([True, False])else(chr(random.randint(65, 90))if random.choice([True, False])else chr(random.randint(97, 122))))for _ in range(5))
    return key

async def xor_cipher(text: str, key: str):
    '''
    Encrypts the text to base64 using the XOR cipher with the key
    '''
    cipher_bytes = bytearray()
    key_length = len(key)
    for i, char in enumerate(text):
        text_byte = ord(char)                                      # convert char to byte
        key_byte = ord(key[i % key_length])                        # convert key to byte
        xor_result = text_byte ^ key_byte                          # XOR text byte and key byte
        cipher_bytes.append(xor_result)                            # store to bytearray
    cipher_base64 = base64.b64encode(cipher_bytes).decode("utf-8") # encode byte array to base64
    return cipher_base64

async def xor_decipher(cipher: str, key: str):
    '''
    Decrypts the base64 encoded XOR cipher with the key
    '''
    cipher_bytes = base64.b64decode(cipher)
    text = ""
    key_length = len(key)
    for i, byte in enumerate(cipher_bytes):
        xor_result = byte ^ ord(key[i % key_length])
        text += chr(xor_result)
    return text