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


class TestDeleteCommand(unittest.TestCase):
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

    def test_delete_with_empty_database(self):
        # startup BOT and DATABASE
        postgres_startup()
        bot_startup()

        # wait for BOT and DATABASE environments startup
        time.sleep(env_wait)

        # check that database empty before test
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 0)

        # make HTTP request to BOT to delete product
        respose = requests.post(
            url="http://localhost:8989/delete",
            json={
                "product_url": "https://www.wb.ru/1",
                "user_id": "55555",
            }
        )

        # check failed BOT responce
        self.assertEqual(respose.status_code, 404)
        self.assertEqual(
            respose.json(),
            {
                "url": "https://www.wb.ru/1",
                "user_id": 55555,
                "bot_send_message_text": "",
                "bot_reply_to_text": "failed to delete product: not found",
            } 
        )

        # cleanup environment for other tests
        bot_shutdown()
        postgres_shutdown()

    def test_delete_current_user_product(self):
        # startup BOT and DATABASE
        postgres_startup()
        bot_startup()

        # wait for BOT and DATABASE environments startup
        time.sleep(env_wait)

        # add product for current user to DATABASE
        insert_into_products(
            pgdsn=self.pgdsn,
            sql_request=(
                f"INSERT INTO products (url, title, vendor, user_telegram_id) "
                f"VALUES "
                f"('https://www.wb.ru/1', 'test_title1', 'test_vendor1', '55555')"
            ),
        )

        # check that product was acually added to DATABASE
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 1)

        # make HTTP request to BOT to delete product
        respose = requests.post(
            url="http://localhost:8989/delete",
            json={
                "product_url": "https://www.wb.ru/1",
                "user_id": "55555",
            }
        )

        # check succeed BOT responce
        self.assertEqual(respose.status_code, 200)
        self.assertEqual(
            respose.json(),
            {
                "url": "https://www.wb.ru/1",
                "user_id": 55555,
                "bot_send_message_text": "successfully deleted product from database",
                "bot_reply_to_text": "",
            } 
        )

        # check that product was acutally deleted from DATABASE
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 0)

        # cleanup environment for other tests
        bot_shutdown()
        postgres_shutdown()

    def test_delete_different_user_product(self):
        # startup BOT and DATABASE
        postgres_startup()
        bot_startup()

        # wait for BOT and DATABASE environments startup
        time.sleep(env_wait)

        # add products for other user to DATABASE
        insert_into_products(
            pgdsn=self.pgdsn,
            sql_request=(
                f"INSERT INTO products (url, title, vendor, user_telegram_id) "
                f"VALUES "
                f"('https://www.wb.ru/1', 'test_title1', 'test_vendor1', '22222')"
            ),
        )

        # check that product was acually added to DATABASE
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 1)

        # make HTTP request to BOT to delete product of current user
        respose = requests.post(
            url="http://localhost:8989/delete",
            json={
                "product_url": "https://www.wb.ru/1",
                "user_id": "11111",
            }
        )

        # check failed BOT responce
        self.assertEqual(respose.status_code, 404)
        self.assertEqual(
            respose.json(),
            {
                "url": "https://www.wb.ru/1",
                "user_id": 11111,
                "bot_send_message_text": "",
                "bot_reply_to_text": "failed to delete product: not found",
            } 
        )

        # check that product of other user actually was not deleted from DATABASE
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "https://www.wb.ru/1")
        self.assertEqual(rows[0][1], "test_title1")
        self.assertEqual(rows[0][2], "test_vendor1")
        self.assertEqual(rows[0][3], "22222")

        # cleanup environment for other tests
        bot_shutdown()
        postgres_shutdown()

    def test_delete_unexisting_product(self):
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
                f"('https://www.wb.ru/1', 'test_title1', 'test_vendor1', '55555'), "
                f"('https://www.wb.ru/2', 'test_title2', 'test_vendor2', '55555'), "
                f"('https://www.wb.ru/3', 'test_title3', 'test_vendor3', '55555')"
            ),
        )

        # check that products was actually added to DATABASE
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 3)

        # make HTTP request to BOT to delete unexisting product
        respose = requests.post(
            url="http://localhost:8989/delete",
            json={
                "product_url": "https://www.wb.ru/4",
                "user_id": "55555",
            }
        )

        # check failed BOT responce
        self.assertEqual(respose.status_code, 404)
        self.assertEqual(
            respose.json(),
            {
                "url": "https://www.wb.ru/4",
                "user_id": 55555,
                "bot_send_message_text": "",
                "bot_reply_to_text": "failed to delete product: not found",
            } 
        )

        # check that no products was deleted from DATABASE
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 3)

        # cleanup environment for other tests
        bot_shutdown()
        postgres_shutdown()

    def test_delete_without_database_available(self):
        # startup only BOT
        bot_startup()

        # wait for BOT startup
        time.sleep(env_wait)

        # check that DATABASE actually not avaliable
        with self.assertRaises(Exception) as ex:
            with psycopg2.connect(self.pgdsn) as conn:
                pass

        # make HTTP request to BOT to delete product
        respose = requests.post(
            url="http://localhost:8989/delete",
            json={
                "product_url": "https://www.wb.ru/1",
                "user_id": "55555",
            }
        )

        # check failed BOT responce
        self.assertEqual(respose.status_code, 500)
        self.assertEqual(
            respose.json(),
            {
                "url": "https://www.wb.ru/1",
                "user_id": 55555,
                "bot_send_message_text": "",
                "bot_reply_to_text": "failed to delete product: database error",
            } 
        )

        # cleanup environment for other tests
        bot_shutdown()
