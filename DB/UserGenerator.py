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
from faker import Faker

ssl._create_default_https_context = ssl._create_unverified_context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="postgres", port=5432)
cur = conn.cursor()


def get_hashed_password(password):
    return pwd_context.hash(password)


def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y', prop)


def random_datetime(day_delta=30):
    day_delta = random.randint(0, day_delta)
    hour_delta = random.randint(0, 23)
    min_delta = random.randint(0, 59)
    sec_delta = random.randint(0, 59)
    return datetime.datetime.now() - datetime.timedelta(days=day_delta, hours=hour_delta, minutes=min_delta,
                                                        seconds=sec_delta)


def create_fake_user_data(amount):
    user_list = RandomUser.generate_users(amount)
    users = []

    for user in user_list:
        username = user.get_username()
        password = user.get_password()
        hashed_password = get_hashed_password(password)
        email = user.get_email()
        create_date = random_date("1/1/2023 1:30 PM", "5/8/2023 4:50 AM", random.random())
        female_name = namer.generate(False)

        user_data = {
            "account_id": username,
            "hashed_password": hashed_password,
            "name": female_name,
            "email": email,
            "create_date": create_date,
            "last_access": random_datetime()
        }
        users.append(user_data)

    return users


def create_fake_customer(amount):
    rank_codes = ['A', 'B', 'C']

    blood_types = ['A', 'B', 'O', 'AB']

    for i in range(amount):
        customer = Faker('ko-KR')

        rank_code = rank_codes[random.randint(0, 2)]
        name = customer.name()
        birthday = random_date("1/1/1965", "5/8/2004", random.random())
        job = customer.job()
        blood_type = blood_types[random.randint(0, 3)]
        contact = customer.phone_number()
        is_married = bool(random.getrandbits(1))
        if is_married:
            child_amt = random.randint(0, 3)
        else:
            child_amt = 0
        home_address = customer.address()
        work_address = customer.company()

        attributes = ['rank_code', 'name', 'birthday', 'job', 'blood_type', 'contact', 'is_married', 'child_amt', 'home_address',
                       'work_address']

        attributes = str(attributes).removeprefix("[").removesuffix("]").replace("'", "")

        result_list = [rank_code, name, birthday, job, blood_type, contact, is_married, child_amt, home_address,
                       work_address]

        result_list = list(map(lambda x: f"'{x}'", result_list))
        result = str(result_list).replace("\"", "").removeprefix("[").removesuffix("]")

        query = f"INSERT INTO CUSTOMER_TB ({attributes}) VALUES ({result})"
        print("[INSERT]", result)
        cur.execute(query)
        conn.commit()


create_fake_customer(int(input("Input Test User Amount: ")))
