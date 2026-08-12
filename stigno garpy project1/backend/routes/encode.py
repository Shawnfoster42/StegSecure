import os
import base64
import hashlib
from cryptography.fernet import Fernet
from ..utils.lsb_encoder import encode_image, encode_audio


# ----------------- Helper: Password → Fernet Key -----------------
def password_to_key(password: str) -> bytes:
    """
    Convert password into a valid Fernet key
    """
    hashed = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hashed)


# ----------------- Video Encryption -----------------
def encrypt_bytes(data: bytes, password: str) -> bytes:
    key = password_to_key(password)
    fernet = Fernet(key)
    return fernet.encrypt(data)


def encode_video(input_path, output_path, password):
    """Encrypt entire video file (no steganography)."""
    with open(input_path, "rb") as f:
        data = f.read()

    encrypted_data = encrypt_bytes(data, password)

    with open(output_path, "wb") as f:
        f.write(encrypted_data)


# ----------------- Main Encode Function -----------------
def encode_file(filepath, message, password=None):
    ext = filepath.split('.')[-1].lower()
    output_path = filepath.rsplit('.', 1)[0] + '_enc.' + ext

    try:
        # --- Images ---
        if ext in ['png', 'bmp']:
            encode_image(filepath, output_path, message, password)

        elif ext in ['jpg', 'jpeg']:
            raise ValueError("JPEG is lossy. Use PNG or BMP.")

        # --- Audio ---
        elif ext == 'wav':
            encode_audio(filepath, output_path, message, password)

        elif ext == 'mp3':
            raise ValueError("MP3 not supported. Use WAV.")

        # --- Video ---
        elif ext in ['avi', 'mov', 'mp4']:
            if not password:
                raise ValueError("Password required for video encryption.")
            encode_video(filepath, output_path, password)

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    except Exception as e:
        raise RuntimeError(f"Encoding failed for {filepath}: {e}")

    return output_path
