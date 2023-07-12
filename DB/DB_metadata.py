# pip install korean-name-generator
# pip install randomuser
# pip install bcrypt
# pip install passlib
# pip install psycopg2-binary
# pip install Faker # REF: https://wikidocs.net/105448

import datetime
from randomuser import RandomUser
import random
import time
import ssl
from pprint import pprint
import csv
from korean_name_generator import namer
from passlib.context import CryptContext
import psycopg2
import clipboard
from faker import Faker

ssl._create_default_https_context = ssl._create_unverified_context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="postgres", port=5432)
cur = conn.cursor()


def get_table_attributes():

    # 테이블 이름과 속성 조회 쿼리 실행
    cur.execute("""
        SELECT table_name, column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
    """)

    results = cur.fetchall()

    # 테이블 이름을 키로 가지는 딕셔너리 생성
    table_attributes = {}

    for table_name, column_name in results:
        if table_name not in table_attributes:
            table_attributes[table_name] = []
        table_attributes[table_name].append(column_name)

    cur.close()
    return table_attributes


def capitalize_first_letter(input_string):
    if len(input_string) > 0:
        return input_string[0].upper() + input_string[1:]
    else:
        return input_string


# 테이블 이름과 속성 조회
table_attributes_dict = get_table_attributes()
result = ""

# 결과 출력
for table_name, attributes in table_attributes_dict.items():
    cur = conn.cursor()
    query = f"SELECT a.attname FROM pg_index i JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey) WHERE i.indrelid = '{table_name}'::regclass AND i.indisprimary"
    cur.execute(query)
    primary_keys = [row[0] for row in cur.fetchall()]

    class_name = table_name.removesuffix("_tb")
    class_name = capitalize_first_letter(class_name)

    class_definition_text = f"class {class_name}:"
    class_definition_text += f"\n\t__table_name__ = '{table_name}'"
    class_definition_text += f"\n\t__primary_keys__ = {primary_keys}\n"
    for attribute in sorted(attributes):
        class_definition_text += f"\n\t{attribute}: str"


    result += class_definition_text + "\n\n\n"

# 연결 종료
conn.close()
clipboard.copy(result)

