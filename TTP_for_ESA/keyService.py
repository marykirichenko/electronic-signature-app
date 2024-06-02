from os import listdir
import errorDefinitions
import requests

class KeyService:
    def __init__(self, pin):
        self.pin = pin
        self.private_key = None
        self.public_key = None

    def getKeys(self):
        try:
            key_gen = requests.post('http://127.0.0.1:5000/generateAndEncrypt', json={'pin': self.pin})
            key_gen = key_gen.json()
            self.private_key = key_gen.get('encrypted_private_key')
            self.public_key = key_gen.get('public_key')
        except Exception:
            raise 'error with key generation'

        # name of the USB flash is 'NO NAME'
        # this code will work only on MAC with NO NAME stick inserted, you should adjust the logic
        # of getting the list of Volumes to your OS
        list_of_volumes = listdir('/Volumes')

        if 'NO NAME' in list_of_volumes:
            if self.private_key:
                usb_drive_path = "/Volumes/NO NAME"
                with open(usb_drive_path+'/key.txt', 'w') as file:
                    file.write(self.private_key)
                with open('/Users/mariiakyrychenko/Desktop/public_key.txt', 'w') as file:
                    file.write(self.public_key)
            else:
                raise errorDefinitions.PrivateKeyDontExist
        else:
            raise errorDefinitions.NoValidUSBDevice

