from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from os import listdir
import errorDefinitions
import base64


class KeyGenerator:
    def __init__(self, pin):
        self.private_key = None
        self.key_length = None
        self.public_key = None
        self.cipher_text = None
        self.iv = None
        self.pin = pin

    def generate_keys(self):
        key = RSA.generate(4096)
        self.private_key = key.export_key()
        self.public_key = key.publickey().export_key()

    def encrypt_private_key(self):
        cipher = AES.new(PBKDF2(self.pin, b'salt', 16, count=1000000), AES.MODE_CBC)
        self.cipher_text = cipher.encrypt(pad(self.private_key, AES.block_size))
        self.iv = cipher.iv

    def decrypt_private_key(self):
        aes_key = PBKDF2(self.pin, b'salt', 16, count=1000000)
        cipher = AES.new(aes_key, AES.MODE_CBC, self.iv)
        decrypted_data = cipher.decrypt(self.cipher_text)
        original_data = unpad(decrypted_data, AES.block_size)
        print("Decrypted private key:", original_data.decode('utf-8'))


    def write_keys_to_file(self):
        # name of the USB flash is 'NO NAME'
        # this code will work only on MAC with NO NAME stick inserted, you should adjust the logic
        # of getting the list of Volumes to your OS
        list_of_volumes = listdir('/Volumes')
        if 'NO NAME' in list_of_volumes:
            self.generate_keys()
            self.encrypt_private_key()
            if self.private_key:
                usb_drive_path = "/Volumes/NO NAME"
                with open(usb_drive_path+'/key.txt', 'w') as file:
                    file.write(base64.b64encode(self.cipher_text).decode('utf-8'))
                with open('/Users/mariiakyrychenko/Desktop/public_key.txt', 'w') as file:
                    file.write(base64.b64encode(self.public_key).decode('utf-8'))
                # print(self.private_key)
                # self.decrypt_private_key()
            else:
                raise  errorDefinitions.PrivateKeyDontExist
        else:
            raise errorDefinitions.NoValidUSBDevice

        print("before encryption     " + str(self.private_key))

