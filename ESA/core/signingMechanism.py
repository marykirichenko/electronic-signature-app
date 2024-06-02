import mimetypes
import getpass
from datetime import datetime
from lxml import etree
import base64
from utils.keyRetrieval import privateKeyRetrieval, publicKeyRetrieval
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import os


class SigningMechanism:
    def __init__(self, pin, filepath):
        self.pin = pin
        self.filepath = filepath
    def encrypt_file_hash(self):
        try:
            private_key = privateKeyRetrieval(self.pin)
            private_key = RSA.import_key(private_key)

            with open(self.filepath, 'rb') as file:
                data = file.read()
                hasher = SHA256.new()
                hasher.update(data)
                digest = hasher.digest()

            signer = pkcs1_15.new(private_key)
            signature = signer.sign(SHA256.new(digest))

            return signature
        except Exception as e:
            raise e

    def extract_file_metadata(self):
        try:
            size = os.path.getsize(self.filepath)
            print('size extracted')
            extension = mimetypes.guess_extension(mimetypes.guess_type(self.filepath)[0])
            modification_time = datetime.fromtimestamp(os.path.getmtime(self.filepath))
            print('metadata extracted')
            return size, extension, modification_time

        except Exception as e:
            raise e

    def create_xml_signature(self):
        try:
            private_key = privateKeyRetrieval(self.pin)
            private_key = RSA.import_key(private_key)

            with open(self.filepath, 'rb') as file:
                data = file.read()
                hasher = SHA256.new()
                hasher.update(data)
                digest = hasher.digest()

            signer = pkcs1_15.new(private_key)
            signature = signer.sign(SHA256.new(digest))

            size, extension, modification_time = self.extract_file_metadata()
            root = etree.Element('Signature')
            doc_info = etree.SubElement(root, 'DocumentInfo')
            etree.SubElement(doc_info, 'Size').text = str(size)
            etree.SubElement(doc_info, 'Extension').text = extension
            etree.SubElement(doc_info, 'ModificationTime').text = modification_time.isoformat()
            user_info_element = etree.SubElement(root, 'UserInfo')
            etree.SubElement(user_info_element, 'user_name').text = getpass.getuser()
            signature_element = etree.SubElement(root, 'SignatureValue')
            signature_element.text = base64.b64encode(signature).decode()
            timestamp = etree.SubElement(root, 'Timestamp')
            timestamp.text = datetime.now().isoformat()

            tree = etree.ElementTree(root)
            tree.write(self.filepath[:self.filepath.rfind('/')] + '/filesignature.xml', pretty_print=True,
                       xml_declaration=True, encoding='UTF-8')
        except Exception as e:
            raise e

    def verify_xml_signature(self, signature_file):
        try:
            public_key = publicKeyRetrieval()
            public_key = RSA.import_key(public_key)

            with open(signature_file, 'rb') as file:
                data = file.read()
                root = etree.fromstring(data)
                signature = base64.b64decode(root.find('SignatureValue').text)

            with open(self.filepath, 'rb') as file:
                data = file.read()
                hasher = SHA256.new()
                hasher.update(data)
                original_hash = hasher.digest()

            verifier = pkcs1_15.new(public_key)
            verifier.verify(SHA256.new(original_hash), signature)
            return True
        except Exception as e:
            return False
#
# print(SigningMechanism('11111111','/Users/mariiakyrychenko/Desktop/public_key.txt').create_xml_signature())
# print(SigningMechanism('11111111','/Users/mariiakyrychenko/Desktop/public_key.txt').verify_xml_signature('/Users/mariiakyrychenko/Desktop/filesignature.xml'))