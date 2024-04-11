# define Python user-defined exceptions
class NoValidUSBDevice(Exception):
    "No valid key-device were inserted"
    pass

class PrivateKeyDontExist(Exception):
    "Private key wasn't passed or generated"
    pass

