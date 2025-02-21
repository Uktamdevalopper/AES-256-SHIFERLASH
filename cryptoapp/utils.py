from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

AES_KEY_SIZE = 32  # AES-256 uchun 32 bayt
BLOCK_SIZE = AES.block_size  # 16 bayt

def encrypt_text(text, key):
    """Matnni AES-256 bilan shifrlaydi va IV + shifrlangan malumotni qaytaradi."""
    if len(key) not in [16, 24, 32]:
        raise ValueError("AES kaliti uzunligi 16, 24 yoki 32 bayt bo‘lishi kerak!")

    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(text.encode(), BLOCK_SIZE))
    return iv + encrypted_data  # IV va shifrlangan malumotni birlashtiramiz

def decrypt_text(encrypted_data, key):
    """AES-256 shifrlangan malumotni deshifrlaydi."""
    iv = encrypted_data[:BLOCK_SIZE]  # IV ni ajratib olamiz
    encrypted_text = encrypted_data[BLOCK_SIZE:]  # Asl shifrlangan ma'lumot

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_text), BLOCK_SIZE)
    return decrypted_data.decode()
