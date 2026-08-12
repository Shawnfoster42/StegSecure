import os
from ..utils.lsb_decoder import decode_image, decode_audio
from cryptography.fernet import Fernet

def decrypt_bytes(data, password):
    key = Fernet(password.encode().ljust(32, b'0')[:32])
    f = Fernet(key._signing_key[:32])
    return f.decrypt(data)

def decode_video(input_path, password):
    if not password:
        raise ValueError("Password required for video decryption.")
    with open(input_path, "rb") as f:
        encrypted_data = f.read()
    return decrypt_bytes(encrypted_data, password)

def decode_file(filepath, password=None):
    ext = filepath.split('.')[-1].lower()

    if ext in ['png', 'bmp']:
        return decode_image(filepath, password)

    elif ext == 'wav':
        return decode_audio(filepath, password)

    elif ext in ['avi', 'mp4', 'mov']:
        return decode_video(filepath, password)

    else:
        raise ValueError("Unsupported file type")
