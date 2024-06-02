import os
import requests
from utils.errorDefinitions import FileNotFoundError


def privateKeyRetrieval(pin):
    usb_drive_path = "/Volumes/NO NAME"
    if not os.path.exists(usb_drive_path + '/key.txt'):
        raise FileNotFoundError
    try:
        with open(usb_drive_path + '/key.txt', 'r') as file:
            encrypted_private_key = file.read()
    except Exception as e:
        raise Exception("An error occurred while reading the file.")
    try:
        decrypted_private_key = requests.post('http://127.0.0.1:5000/decrypt',
                                              json={'pin': pin, 'cipher_text': encrypted_private_key})
        return bytes(decrypted_private_key.json().get('private_key'), 'utf-8')
    except Exception as e:
        raise Exception("An error occurred while decrypting file.")


def publicKeyRetrieval():
    try:
        with open('/Users/mariiakyrychenko/Desktop/public_key.txt', 'rb') as file:
            return file.read()
    except Exception as e:
        raise Exception("An error occurred while reading the file.")
