# pip install rsa
import rsa


def spell_print(text):
    print(f"[{len(text)} spells]", text)


class RSA:
    def __init__(self, public_key_path="Public.key", private_key_path="Private.key", gen_key=True):
        self.public_key_path = public_key_path
        self.private_key_path = private_key_path

        self.private_key = None
        self.public_key = None

        if gen_key:
            self.generate_key()
        else:
            self.load_key()


    def generate_key(self):
        (self.public_key, self.private_key) = rsa.newkeys(1024)
        with open(self.public_key_path, 'wb') as file:
            file.write(self.public_key.save_pkcs1('PEM'))

        with open(self.private_key_path, 'wb') as file:
            file.write(self.private_key.save_pkcs1('PEM'))

    def load_key(self):
        with open(self.public_key_path, 'rb') as file:
            self.public_key = rsa.PublicKey.load_pkcs1(file.read())

        with open(self.private_key_path, 'rb') as file:
            self.private_key = rsa.PrivateKey.load_pkcs1(file.read())


    def encrypt(self, plain_text):
        return rsa.encrypt(plain_text, self.public_key)


    def decrypt(self, cipher_text):
        try:
            return rsa.decrypt(cipher_text, self.private_key)
        except Exception as e:
            print(e)
            return False


    def file_encrypt(self, path):
        cipher_text = b""
        with open(path, "rb") as f:
            while (byte := f.read(117)):
                enc_text = self.encrypt(byte)
                print(f"{byte} -> {enc_text}")
                cipher_text += enc_text

        with open(path, "wb") as f:
            f.write(cipher_text)


    def file_decrypt(self, path):
        plain_text = b""
        with open(path, "rb") as f:
            while (byte := f.read(128)):
                dec_text = self.decrypt(byte)
                print(f"{byte} -> {dec_text}")
                plain_text += dec_text

        with open(path, "wb") as f:
            f.write(plain_text)

    def sign(self, message):
        return rsa.sign(message.encode(), self.private_key, 'SHA-1')

    def verify(self, message, signature):
        try:
            return rsa.verify(message.encode(), signature, self.public_key) == 'SHA-1'
        except Exception as e:
            print(e)
            return False

rsa_obj = RSA(gen_key=False)
#rsa_obj.file_encrypt("6월4주차.pdf")
rsa_obj.file_decrypt("6월4주차.pdf")

