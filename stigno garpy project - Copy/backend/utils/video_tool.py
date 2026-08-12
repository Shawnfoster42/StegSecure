from cryptography.fernet import Fernet
import hashlib, base64

def generate_key(password: str) -> bytes:
    digest = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(digest)

def encrypt_video_file(input_path: str, output_path: str, password: str):
    key = generate_key(password)
    f = Fernet(key)
    with open(input_path, "rb") as f_in:
        data = f_in.read()
    encrypted = f.encrypt(data)
    with open(output_path, "wb") as f_out:
        f_out.write(encrypted)

def decrypt_video_file(input_path: str, output_path: str, password: str):
    key = generate_key(password)
    f = Fernet(key)
    with open(input_path, "rb") as f_in:
        data = f_in.read()
    decrypted = f.decrypt(data)
    with open(output_path, "wb") as f_out:
        f_out.write(decrypted)
