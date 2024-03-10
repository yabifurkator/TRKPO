import os
import time
import requests

import psycopg2


env_wait = 1


def bot_startup():
    os.system("cd ../../ && docker compose up -d bot")


def bot_shutdown():
    os.system("cd ../../ && docker compose down bot --timeout 1")


def postgres_startup():
    os.system("cd ../../ && docker compose up --force-recreate -d database")


def postgres_shutdown():
    os.system("cd ../../ && docker compose down database --timeout 1")


def select_from_products(pgdsn: str) -> list[tuple]:
    with psycopg2.connect(pgdsn) as conn:
        with conn.cursor() as curs:
            curs.execute("SELECT url, title, vendor, user_telegram_id FROM products")

            return curs.fetchall()
        

def insert_into_products(pgdsn: str, sql_request: str):
    with psycopg2.connect(pgdsn) as conn:
        with conn.cursor() as curs:
            curs.execute(sql_request)
            conn.commit()


def wait_for_connection(waiting_seconds: int):
    init_time = time.time()
    while True:
        try: 
            response = requests.get("http://127.0.0.1:8989/ping")
            if response.status_code == 200:
                time.sleep(1.0)
                return
            else:
                raise Exception(f"status code not 200 ({response.status_code})")
        except Exception:
            current_time = time.time()
            if current_time - init_time > waiting_seconds:
                raise Exception("waiting for connection timed out")
            time.sleep(0.1)
