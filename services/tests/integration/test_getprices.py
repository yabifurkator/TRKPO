import os
import time
import unittest
import requests

import psycopg2

from .common import \
    postgres_startup, \
    postgres_shutdown, \
    bot_startup, \
    bot_shutdown, \
    env_wait, \
    select_from_products, \
    insert_into_products


class TestGetpricesCommand(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        os.environ["POSTGRES_USER"] = "username"
        os.environ["POSTGRES_PASSWORD"] = "password"
        os.environ["POSTGRES_DB"] = "database"
        os.environ["BOT_TOKEN"] = "6145919547:AAHW9NdlxISaPfNQnUA8gmShYFpYRWz8s_g"

        self.pgdsn = (
            "postgres://"
            "testuser:testpassword@"
            "127.0.0.1:5432/database?"
            "sslmode=disable&gssencmode=disable"
        )

    def test_empty_database(self):
        # startup BOT and DATABASE
        postgres_startup()
        bot_startup()

        # wait for BOT and DATABASE environments startup
        time.sleep(env_wait)

        # check that DATABASE actually empty
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 0)

        # make HTTP request to BOT to get prices
        respose = requests.post(
            url="http://localhost:8989/getprices",
            json={
                "user_id": "55555",
            } 
        )

        # check failed BOT responce
        self.assertEqual(respose.status_code, 404)
        self.assertEqual(
            respose.json(),
            {
                "user_id": 55555,
                "bot_send_message_text": "prices:\n----------------------\nnot found",
                "bot_reply_to_text": "",
            } 
        )

        # cleanup environment for other tests
        bot_shutdown()
        postgres_shutdown()

    def test_current_user_have_products(self):
        # startup BOT and DATABASE
        postgres_startup()
        bot_startup()

        # wait for BOT and DATABASE environments startup
        time.sleep(env_wait)

        # add products for current user to DATABASE
        insert_into_products(
            pgdsn=self.pgdsn,
            sql_request=(
                f"INSERT INTO products (url, title, vendor, user_telegram_id) "
                f"VALUES "
                f"('https://www.wb.ru/1', 'test_title1', 'test_vendor1', '55555'),"
                f"('https://www.wb.ru/2', 'test_title2', 'test_vendor2', '55555'),"
                f"('https://www.wb.ru/3', 'test_title3', 'test_vendor3', '55555')"
            ),
        )

        # check that products was actually added to DATABASE
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 3)

        # make HTTP request to BOT for get prices
        respose = requests.post(
            url="http://localhost:8989/getprices",
            json={
                "user_id": "55555",
            } 
        )

        # check succeed BOT responce
        self.assertEqual(respose.status_code, 200)
        self.assertEqual(
            respose.json(),
            {
                "user_id": 55555,
                "bot_send_message_text": (
                    "prices:\n"
                    "----------------------\n"
                    "Product:\n - url: https://www.wb.ru/1\n - title: test_title1\n - vendor: test_vendor1\n - price: 999\n"
                    "----------------------\n"
                    "Product:\n - url: https://www.wb.ru/2\n - title: test_title2\n - vendor: test_vendor2\n - price: 999\n"
                    "----------------------\n"
                    "Product:\n - url: https://www.wb.ru/3\n - title: test_title3\n - vendor: test_vendor3\n - price: 999\n"
                    "----------------------"
                ),
                "bot_reply_to_text": "",
            } 
        )

        # cleanup environment for other tests
        bot_shutdown()
        postgres_shutdown()

    def test_different_user_have_products(self):
        # startup BOT and DATABASE
        postgres_startup()
        bot_startup()

        # wait for BOT and DATABASE environments startup
        time.sleep(env_wait)

        # add products for other users to DATABASE
        insert_into_products(
            pgdsn=self.pgdsn,
            sql_request=(
                f"INSERT INTO products (url, title, vendor, user_telegram_id) "
                f"VALUES "
                f"('https://www.wb.ru/1', 'test_title1', 'test_vendor1', '22222'),"
                f"('https://www.wb.ru/1', 'test_title1', 'test_vendor1', '33333'),"
                f"('https://www.wb.ru/1', 'test_title1', 'test_vendor1', '44444')"
            ),
        )

        # check that products was actually added to database
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 3)

        # make HTTP request to BOT for get prices for current user
        respose = requests.post(
            url="http://localhost:8989/getprices",
            json={
                "user_id": "11111",
            } 
        )

        # check 404 BOT responce
        self.assertEqual(respose.status_code, 404)
        self.assertEqual(
            respose.json(),
            {
                "user_id": 11111,
                "bot_send_message_text": "prices:\n----------------------\nnot found",
                "bot_reply_to_text": "",
            } 
        )

        # cleanup environment for other tests
        bot_shutdown()
        postgres_shutdown()

    def test_with_wildberries_exception(self):
        # startup BOT and DATABASE
        postgres_startup()
        bot_startup()

        # wait for BOT and DATABASE environments startup
        time.sleep(env_wait)

        # add products for current user (with exception behaviour) to DATABASE
        insert_into_products(
            pgdsn=self.pgdsn,
            sql_request=(
                f"INSERT INTO products (url, title, vendor, user_telegram_id) "
                f"VALUES "
                f"('https://www.wb.ru/1', 'wildberries_exception', 'test_vendor1', '55555'),"
                f"('https://www.wb.ru/2', 'test_title2',           'test_vendor2', '55555'),"
                f"('https://www.wb.ru/3', 'test_title3',           'test_vendor3', '55555')"
            ),
        )

        # check that products was actually added to DATABASE
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 3)

        # make HTTP request to BOT for get prices
        respose = requests.post(
            url="http://localhost:8989/getprices",
            json={
                "user_id": "55555",
            } 
        )

        # check failed BOT responce
        self.assertEqual(respose.status_code, 500)
        self.assertEqual(
            respose.json(),
            {
                "user_id": 55555,
                "bot_send_message_text": "",
                "bot_reply_to_text": "failed to get prices: unknown exception: unexpected exception on wildberries side",
            } 
        )

        # cleanup environment for other tests
        bot_shutdown()
        postgres_shutdown()

    def test_getprices_without_database_available(self):
        # startup only BOT
        bot_startup()

        # wait for BOT startup
        time.sleep(env_wait)

        # check that DATABASE actually not avaliable
        with self.assertRaises(Exception) as ex:
            with psycopg2.connect(self.pgdsn) as conn:
                pass

        # make HTTP request to BOT to get prices
        respose = requests.post(
            url="http://localhost:8989/getprices",
            json={
                "product_url": "https://www.wb.ru",
                "user_id": "55555",
            }
        )

        # check failed BOT responce
        self.assertEqual(respose.status_code, 500)
        self.assertEqual(
            respose.json(),
            {
                "user_id": 55555,
                "bot_send_message_text": "",
                "bot_reply_to_text": "failed to get prices: database error",
            } 
        )

        # cleanup environment for other tests
        bot_shutdown()
