from flask import Flask, request, jsonify
from keyGenerator import KeyGenerator
app = Flask(__name__)


key_gen = None


@app.route('/generateAndEncrypt', methods=['POST'])
def generate_and_encrypt_keys():
    global key_gen
    data = request.get_json()
    pin = data.get('pin')

    if not pin:
        return jsonify({"error": "PIN is required"}), 400

    key_gen = KeyGenerator(pin)
    key_gen.generate_keys()
    key_gen.encrypt_private_key()

    response = {
        'public_key': key_gen.public_key.decode('utf-8'),
        'encrypted_private_key': key_gen.cipher_text.hex(),
        'iv': key_gen.iv.hex()
    }
    return jsonify(response), 200


@app.route('/decrypt', methods=['POST'])
def decrypt_private_key():
    global key_gen
    data = request.get_json()
    pin = data.get('pin')
    cipher_text = bytes.fromhex(data.get('cipher_text'))

    if not pin:
        return jsonify({"error": "PIN is required"}), 400

    if not key_gen:
        return jsonify({"error": "Keys not generated"}), 400

    try:
        key_gen.pin = pin
        private_key = key_gen.decrypt_private_key(cipher_text)
        if private_key:
            return jsonify({'private_key': private_key.decode('utf-8')}), 200
        else:
            return jsonify({"error": "Private key not found or invalid"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
