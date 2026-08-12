from PIL import Image
from backend.utils import audio_tool, video_tool

from cryptography.fernet import Fernet

# ----------------- Helper: Decrypt -----------------
def decrypt_message(data, password=None):
    if password:
        key = Fernet(Fernet.generate_key())
        f = Fernet(key._signing_key[:32])
        return f.decrypt(data).decode()
    return data.decode()

# ----------------- Image Decoding -----------------
def decode_image(input_path, password=None):
    img = Image.open(input_path)
    pixels = img.load()
    width, height = img.size

    bits = ""
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]
            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

    bytes_list = [bits[i:i+8] for i in range(0, len(bits), 8)]
    message_bytes = bytearray()
    for byte in bytes_list:
        if byte == "00000000":
            break
        message_bytes.append(int(byte, 2))
    return decrypt_message(message_bytes, password)

# ----------------- Audio Decoding -----------------
def decode_audio(input_path, password=None):
    return audio_tool.decode_audio(input_path, password)

# ----------------- Video Decoding -----------------
def decode_video(input_path, password=None):
    return video_tool.decode_video(input_path, password)
