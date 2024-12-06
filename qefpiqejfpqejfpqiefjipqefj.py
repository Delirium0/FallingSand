from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Пример шифрования данных
data = b"Test message"
key = get_random_bytes(16)  # 128-битный ключ
cipher = AES.new(key, AES.MODE_EAX)

# Шифрование
ciphertext, tag = cipher.encrypt_and_digest(data)

print(f"Ciphertext: {ciphertext}")
