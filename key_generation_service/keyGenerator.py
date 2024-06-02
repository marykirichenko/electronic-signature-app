from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2


class KeyGenerator:
    def __init__(self, pin):
        self.key_length = None
        self.public_key = None
        self.cipher_text = None
        self.iv = None
        self.pin = pin

    def generate_keys(self):
        key = RSA.generate(4096)
        self.private_key = key.export_key()
        print(self.private_key)
        self.public_key = key.publickey().export_key()
        print(self.public_key)

    def encrypt_private_key(self):
        cipher = AES.new(PBKDF2(self.pin, b'salt', 16, count=1000000), AES.MODE_CBC)
        self.cipher_text = cipher.encrypt(pad(self.private_key, AES.block_size))
        self.iv = cipher.iv

    def decrypt_private_key(self, cipher_text):
        if not cipher_text or not self.iv:
            raise ValueError("Cipher text or IV not found. Make sure to generate and encrypt keys first.")

        try:
            aes_key = PBKDF2(self.pin, b'salt', 16, count=1000000)
            cipher = AES.new(aes_key, AES.MODE_CBC, self.iv)
            decrypted_data = cipher.decrypt(cipher_text)
            original_data = unpad(decrypted_data, AES.block_size)
            return original_data
        except Exception as e:
            raise ValueError("Error decrypting private key:", str(e))
