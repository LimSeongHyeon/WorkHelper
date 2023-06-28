import boto3
import csv
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import time


class KMS:
    def __init__(self, access_key_path, arn=None):
        self.arn = arn

        with open(access_key_path, 'r') as f:
            reader = csv.reader(f)
            reader.__next__()
            access_key, secret_key = reader.__next__()

        self.session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name='ap-northeast-2'
        )
        self.client = self.session.client('kms')

    ''' AWS pricing problems
    def create_CMK(self, alias):
        for current_alias in self.client.list_aliases()['Aliases']:
            if alias == current_alias['AliasName'].removeprefix("alias/"):
                print(f"'{alias}' is already created")
                return None

        # CMK 생성 요청
        response = self.client.create_key()

        # 생성된 CMK의 식별자 출력
        cmk_arn = response['KeyMetadata']['Arn']
        print("CMK ARN:", cmk_arn)

        # CMK에 별칭(Alias) 부여
        alias_name = "alias/" + alias
        alias_response = self.client.create_alias(
            AliasName=alias_name,
            TargetKeyId=cmk_arn
        )
        print(alias_response)

        # 생성된 별칭 출력
        print("Alias ARN:", cmk_arn)
        return cmk_arn
    '''

    def generate_encrypted_data_key(self):
        response = self.client.generate_data_key(
            KeyId=self.arn,
            KeySpec='AES_256'
        )
        # Protect to expose plaintext key
        # plaintext_key = response['Plaintext']
        encrypted_key = response['CiphertextBlob']
        return encrypted_key

    def encrypt_data(self, plaintext, encrypted_key):
        plaintext_key = self.client.decrypt(CiphertextBlob=encrypted_key).get('Plaintext')
        cipher = AES.new(plaintext_key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        iv = b64encode(cipher.iv).decode()
        ciphertext = b64encode(ciphertext).decode()
        return iv, ciphertext

    def decrypt_data(self, iv, ciphertext, encrypted_key):
        plaintext_key = self.client.decrypt(CiphertextBlob=encrypted_key).get('Plaintext')
        cipher = AES.new(plaintext_key, AES.MODE_CBC, b64decode(iv))
        ciphertext = b64decode(ciphertext)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
        return plaintext


start_time = time.time()
kms = KMS("/Users/tommyfuture/Desktop/Jack_accessKeys.csv")
kms.arn = 'arn:aws:kms:ap-northeast-2:252784589582:key/023912b4-6e82-4413-be41-56782c018cdc'


with open("encrypted_key.key", "wb") as f:
    encrypted_key = kms.generate_encrypted_data_key()
    f.write(encrypted_key)

with open("encrypted_text.txt", "wb") as f:
    iv, cipher_text = kms.encrypt_data("1234", encrypted_key)
    f.write(cipher_text.encode())
    print(iv)
