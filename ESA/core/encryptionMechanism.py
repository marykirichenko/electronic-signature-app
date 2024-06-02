from utils.keyRetrieval import privateKeyRetrieval, publicKeyRetrieval
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64

class EncryptionMechanism:

    def encrypt(self, filename):
        try:
            public_key = publicKeyRetrieval()
            with open(filename, 'rb') as file:
                data = file.read()
                cipher_rsa = PKCS1_OAEP.new(RSA.import_key(public_key))
                encrypted_data = cipher_rsa.encrypt(data)
            encoded_data = base64.b64encode(encrypted_data)
            with open(filename[:filename.rfind('/')]+'/encrypted_file.bin', 'wb') as file:  # Open in binary mode
                file.write(encoded_data)
        except Exception as e:
            raise e

    def decrypt(self, filename, pin):
        try:
            private_key = privateKeyRetrieval(pin)
            with open(filename, 'rb') as file:
                encoded_data = file.read()
                encrypted_data = base64.b64decode(encoded_data)
            cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
            decrypted_data = cipher_rsa.decrypt(encrypted_data)
            decrypted_data = decrypted_data.decode('utf-8')
            with open(filename[:filename.rfind('/')]+'/decrypted_file.rtf', 'w') as file:
                file.write(decrypted_data)
        except Exception as e:
            raise e

