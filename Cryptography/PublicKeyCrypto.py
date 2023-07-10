# https://pagichacha.tistory.com/55
# pip install pycryptodome

import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_key_file():
    private_key = RSA.generate(2048)
    print(private_key)
    public_key = private_key.public_key()
    print(public_key)

    with open('private.key', 'wb') as private_key_file:
        private_key_file.write(private_key.export_key('PEM'))
    with open('public.key', 'wb') as public_key_file:
        public_key_file.write(public_key.export_key('PEM'))

def load_key_file(path):
    with open(path, 'rb') as key_file:
        key = RSA.importKey(key_file.read())
        return key

def encrypt_msg(plain_msg, public_key):
    tool = PKCS1_OAEP.new(public_key)
    cypher_msg = tool.encrypt(plain_msg)
    return cypher_msg

def decrypt_msg(cypher_msg, private_key):
    tool = PKCS1_OAEP.new(private_key)
    plain_msg = tool.decrypt(cypher_msg)
    return plain_msg


msg = 'Hello'.encode()

generate_key_file()
public_key = load_key_file("public.key")
enc_msg = encrypt_msg(msg, public_key)
print(len(msg), msg)
print(len(enc_msg), enc_msg)

private_key = load_key_file("private.key")
dec_msg = decrypt_msg(enc_msg, private_key)
print(len(dec_msg), dec_msg)


