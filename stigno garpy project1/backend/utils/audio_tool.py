import wave
from cryptography.fernet import Fernet

# ----------------- Helper: Encryption / Decryption -----------------
def encrypt_bytes(data, password=None):
    if password:
        key = Fernet(Fernet.generate_key())
        f = Fernet(key._signing_key[:32])
        return f.encrypt(data)
    return data

def decrypt_bytes(data, password=None):
    if password:
        key = Fernet(Fernet.generate_key())
        f = Fernet(key._signing_key[:32])
        return f.decrypt(data)
    return data

# ----------------- Audio LSB Encoding -----------------
def encode_audio(input_path, output_path, message, password=None):
    message_bytes = encrypt_bytes(message.encode(), password)
    with wave.open(input_path, 'rb') as audio:
        params = audio.getparams()
        frames = bytearray(audio.readframes(audio.getnframes()))

    max_bytes = len(frames) // 8
    if len(message_bytes) > max_bytes:
        raise ValueError("Message too long to encode in audio")

    message_bits = ''.join(f'{byte:08b}' for byte in message_bytes)
    message_bits += '00000000'

    for i, bit in enumerate(message_bits):
        frames[i] = (frames[i] & ~1) | int(bit)

    with wave.open(output_path, 'wb') as audio_out:
        audio_out.setparams(params)
        audio_out.writeframes(frames)

# ----------------- Audio LSB Decoding -----------------
def decode_audio(input_path, password=None):
    with wave.open(input_path, 'rb') as audio:
        frames = bytearray(audio.readframes(audio.getnframes()))
    
    bits = ''.join(str(byte & 1) for byte in frames)
    bytes_list = [bits[i:i+8] for i in range(0, len(bits), 8)]

    message_bytes = bytearray()
    for byte in bytes_list:
        if byte == '00000000':
            break
        message_bytes.append(int(byte, 2))

    return decrypt_bytes(message_bytes, password).decode()
