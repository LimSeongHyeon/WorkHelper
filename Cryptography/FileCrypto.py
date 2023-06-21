# pip install cryptography
from cryptography.fernet import Fernet
# fernet -> AES-128-CBC


def generate_key_file(keyname):
    with open(f'{keyname}.key', 'wb') as key_file:
        key = Fernet.generate_key()
        key_file.write(key)


def load_key(keyname):
    with open(f'{keyname}.key', 'rb') as key_file:
        return key_file.read()


def encrypt_file(filename, key):
    with open(filename, 'rb') as plain_file:
        plain_bytes = plain_file.read()

    fernet = Fernet(key)
    cypher_bytes = fernet.encrypt(plain_bytes)

    with open(filename, 'wb') as cypher_file:
        cypher_file.write(cypher_bytes)



def decrypt_file(filename, key):
    with open(filename, 'rb') as cypher_file:
        cypher_bytes = cypher_file.read()

    fernet = Fernet(key)
    plain_bytes = fernet.decrypt(cypher_bytes)

    with open(filename, 'wb') as plain_file:
        plain_file.write(plain_bytes)



# generate_key_file("test")
key = load_key("test")
encrypt_file("test.txt", key)
#decrypt_file("test.txt", key)
