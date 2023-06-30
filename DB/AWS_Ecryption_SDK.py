import aws_encryption_sdk
from aws_encryption_sdk import CommitmentPolicy
import boto3
import csv
import botocore.session
from pprint import pprint
from icecream import ic
from datetime import datetime

def time_format():
    return f'[{datetime.now()}] '

ic.configureOutput(prefix=time_format)

# AES-256-GCM (SHA 512)
class AWS_Crypto:
    def __init__(self, alias:str=None, arn:str=None, session:botocore.session=None):
        if alias is None and arn is None:
            raise ValueError("alias and arn are None.")

        if arn:
            self.key_arn = arn
        else:
            self.key_arn = self.get_cmk_arn(alias)
        self.client = aws_encryption_sdk.EncryptionSDKClient(
            commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT)

        # Create an AWS KMS master key provider
        kms_kwargs = dict(key_ids=[self.key_arn])
        if session is not None:
            kms_kwargs["botocore_session"] = session
        self.master_key_provider = aws_encryption_sdk.StrictAwsKmsMasterKeyProvider(**kms_kwargs)

    def get_cmk_arn(self, alias):
        alias = 'alias/' + alias
        kms_client = boto3.client('kms')
        response = kms_client.list_aliases()
        for alias_entry in response['Aliases']:
            if alias_entry['AliasName'] == alias:
                target_key_id = 'key/' + alias_entry['TargetKeyId']
                arn = alias_entry['AliasArn'].replace(alias, target_key_id)
                return arn
        return None

    def encrypt(self, plain_bytes):
        cipher_bytes, encryptor_header = self.client.encrypt(source=plain_bytes,
                                                             key_provider=self.master_key_provider)
        return cipher_bytes

    def decrypt(self, cipher_bytes):
        plain_bytes, decrypted_header = self.client.decrypt(source=cipher_bytes,
                                                            key_provider=self.master_key_provider)
        return plain_bytes

    def file_encrypt(self, file_path):
        with open(file_path, "rb") as f:
            plain_bytes = f.read()

        cipher_bytes = self.encrypt(plain_bytes)

        with open(file_path, "wb") as f:
            f.write(cipher_bytes)

    def file_decrypt(self, file_path):
        with open(file_path, "rb") as f:
            cipher_bytes = f.read()

        plain_bytes = self.decrypt(cipher_bytes)

        with open(file_path, "wb") as f:
            f.write(plain_bytes)

if __name__ == "__main__":
    session = botocore.session.get_session()
    aws_crypto = AWS_Crypto(alias='TEST_CMK', session=session)

    plain_text = input("plaintext: ")
    cipher_text = aws_crypto.encrypt(plain_text)
    ic(len(cipher_text), cipher_text)

    decrypted_text = aws_crypto.decrypt(cipher_text)
    ic(len(decrypted_text), decrypted_text)
