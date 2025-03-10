import json
from Crypto.Cipher import DES3
import base64
import hashlib
from Crypto.Util.Padding import pad, unpad

def encrypt(plain_text, pass_phrase):
    # Create a 24-byte key using MD5 hash of the passphrase (still using MD5 here for simplicity)
    key = hashlib.md5(pass_phrase.encode()).digest()  # MD5 is 128 bits
    key = key + key[:8]  # Extend to 24 bytes for DES3 (Triple DES)
    
    cipher = DES3.new(key, DES3.MODE_ECB)

    # Pad the plain text to ensure it is a multiple of 8 bytes (PKCS7 padding)
    padded_text = pad(plain_text.encode(), DES3.block_size)
    
    # Encrypt the padded text
    encrypted_text = cipher.encrypt(padded_text)

    # Return the base64-encoded string (ensure padding is correct)
    return base64.b64encode(encrypted_text).decode('utf-8')


def decrypt(encrypted_text, pass_phrase):
    # Create a 24-byte key using MD5 hash of the passphrase (still using MD5 here for simplicity)
    key = hashlib.md5(pass_phrase.encode()).digest()
    key = key + key[:8]  # Extend to 24 bytes for DES3 (Triple DES)
    
    cipher = DES3.new(key, DES3.MODE_ECB)

    # Decode the base64-encoded encrypted text
    try:
        encrypted_data = base64.b64decode(encrypted_text.encode())
    except Exception as e:
        raise ValueError("Base64 decoding error: Invalid base64 string") from e

    # Decrypt the data
    decrypted_data = cipher.decrypt(encrypted_data)

    # Unpad the decrypted data (remove PKCS7 padding)
    decrypted_text = unpad(decrypted_data, DES3.block_size).decode('utf-8')

    # Parse the decrypted text as JSON
    parsed_json = json.loads(decrypted_text)

    return parsed_json
