# pip install psycopg2-binary

from randomuser import RandomUser
import ssl
from passlib.context import CryptContext
import psycopg2
from AWS_Ecryption_SDK import AWS_Crypto
import botocore.session

ssl._create_default_https_context = ssl._create_unverified_context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="postgres", port=5432)
cur = conn.cursor()

session = botocore.session.get_session()
aws_crypto = AWS_Crypto(alias='TEST_CMK', session=session)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def insert_data(amt=1):
    users = RandomUser.generate_users(amt)
    for user in users:
        username = user.get_username()
        encrypted_username = aws_crypto.encrypt(username)
        query = f"INSERT INTO TEST.ENCRYPT_TEST_TB (plain_data, encrypted_data) VALUES (%s, %s)"
        values = (username, encrypted_username)
        cur.execute(query, values)
        conn.commit()
        print(f"{bcolors.OKBLUE}{username}{bcolors.ENDC} >>> {bcolors.FAIL}{encrypted_username}{bcolors.ENDC}\n")

def compare_test_case():
    query = "SELECT * FROM TEST.ENCRYPT_TEST_TB"
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        encrypted_bytes = bytes(row[2])
        decrypted_bytes = aws_crypto.decrypt(encrypted_bytes)

        print(f"{bcolors.FAIL}{encrypted_bytes}{bcolors.ENDC} >>> {bcolors.OKBLUE}{decrypted_bytes.decode()}{bcolors.ENDC}\n")

command = input("input a command: ")
if command == "encrypt":
    insert_data(int(input("Test Data Amount is: ")))
elif command == "decrypt":
    compare_test_case()
