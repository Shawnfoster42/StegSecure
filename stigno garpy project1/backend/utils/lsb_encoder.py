from PIL import Image
from backend.utils import audio_tool, video_tool

from cryptography.fernet import Fernet

# ----------------- Helper: Encryption -----------------
def encrypt_message(message, password=None):
    if password:
        key = Fernet(Fernet.generate_key())
        f = Fernet(key._signing_key[:32])
        return f.encrypt(message.encode())
    return message.encode()

# ----------------- Image Encoding -----------------
def encode_image(input_path, output_path, message, password=None):
    message_bytes = encrypt_message(message, password)
    img = Image.open(input_path)
    encoded = img.copy()
    width, height = img.size
    max_bytes = width * height * 3 // 8

    if len(message_bytes) > max_bytes:
        raise ValueError("Message too long to encode in image")

    message_bits = ''.join(f'{byte:08b}' for byte in message_bytes)
    message_bits += '00000000'  # Null byte terminator

    data_index = 0
    pixels = encoded.load()

    for y in range(height):
        for x in range(width):
            if data_index >= len(message_bits):
                break
            r, g, b = pixels[x, y][:3]
            r = (r & ~1) | int(message_bits[data_index]); data_index += 1
            if data_index < len(message_bits):
                g = (g & ~1) | int(message_bits[data_index]); data_index += 1
            if data_index < len(message_bits):
                b = (b & ~1) | int(message_bits[data_index]); data_index += 1
            pixels[x, y] = (r, g, b)
    encoded.save(output_path)

# ----------------- Audio Encoding -----------------
def encode_audio(input_path, output_path, message, password=None):
    audio_tool.encode_audio(input_path, output_path, message, password)

# ----------------- Video Encoding -----------------
def encode_video(input_path, output_path, message, password=None):
    video_tool.encode_video(input_path, output_path, message, password)
