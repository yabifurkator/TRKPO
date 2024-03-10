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
    select_from_products


class TestAddCommand(unittest.TestCase):
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

    def test_succeed_add(self):
        # startup BOT and DATABASE
        postgres_startup()
        bot_startup()

        # wait for BOT and DATABASE environments startup
        time.sleep(env_wait)

        # check that database empty before test
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 0)

        # make HTTP request to BOT to add new product
        respose = requests.post(
            url="http://localhost:8989/add",
            json={
                "product_url": "https://www.wb.ru",
                "user_id": "55555",
            }
        )

        # check succeed BOT responce
        self.assertEqual(respose.status_code, 200)
        self.assertEqual(
            respose.json(),
            {
                "url": "https://www.wb.ru",
                "user_id": 55555,
                "bot_send_message_text": "successfully added new product to database",
                "bot_reply_to_text": "",
            } 
        )

        # check that product was actually added to DATABASE
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "https://www.wb.ru")
        self.assertEqual(rows[0][1], "mock_title")
        self.assertEqual(rows[0][2], "mock_vendor")
        self.assertEqual(rows[0][3], "55555")

        # cleanup environment for other tests
        bot_shutdown()
        postgres_shutdown()

    def test_dublicate_for_same_user(self):
        # startup BOT and DATABASE
        postgres_startup()
        bot_startup()

        # wait for BOT and DATABASE environments startup
        time.sleep(env_wait)

        # check that database empty before test
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 0)

        # make HTTP request to BOT to add new product (first)
        respose = requests.post(
            url="http://localhost:8989/add",
            json={
                "product_url": "https://www.wb.ru",
                "user_id": "55555",
            } 
        )

        # check succeed BOT responce
        self.assertEqual(respose.status_code, 200)
        self.assertEqual(
            respose.json(),
            {
                "url": "https://www.wb.ru",
                "user_id": 55555,
                "bot_send_message_text": "successfully added new product to database",
                "bot_reply_to_text": "",
            } 
        )

        # check that product was actually added to DATABASE
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "https://www.wb.ru")
        self.assertEqual(rows[0][1], "mock_title")
        self.assertEqual(rows[0][2], "mock_vendor")
        self.assertEqual(rows[0][3], "55555")

        # make HTTP request to BOT to add new product (dublicate)
        respose = requests.post(
            url="http://localhost:8989/add",
            json={
                "product_url": "https://www.wb.ru",
                "user_id": "55555",
            } 
        )

        # check failed BOT responce
        self.assertEqual(respose.status_code, 400)
        self.assertEqual(
            respose.json(),
            {
                "url": "https://www.wb.ru",
                "user_id": 55555,
                "bot_send_message_text": "",
                "bot_reply_to_text": "failed to add new product: already exists"
            }
        )

        # chat that dublicate product NOT added to DATABASE
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 1)

        # cleanup environment for other tests
        bot_shutdown()
        postgres_shutdown()
    
    def test_dublicate_for_different_user(self):
        # startup BOT and DATABASE
        postgres_startup()
        bot_startup()

        # wait for BOT and DATABASE environments startup
        time.sleep(env_wait)

        # check that database empty before test
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 0)

        # make HTTP request to BOT to add new product (first, user_id=11111)
        respose = requests.post(
            url="http://localhost:8989/add",
            json={
                "product_url": "https://www.wb.ru",
                "user_id": "11111",
            } 
        )

        # check succeed BOT responce
        self.assertEqual(respose.status_code, 200)
        self.assertEqual(
            respose.json(),
            {
                "url": "https://www.wb.ru",
                "user_id": 11111,
                "bot_send_message_text": "successfully added new product to database",
                "bot_reply_to_text": "",
            } 
        )

        # check that first product was actually added to DATABASE
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][0], "https://www.wb.ru")
        self.assertEqual(rows[0][1], "mock_title")
        self.assertEqual(rows[0][2], "mock_vendor")
        self.assertEqual(rows[0][3], "11111") # check first user_id

        # make HTTP request to BOT to add new product (second, user_id=22222)
        respose = requests.post(
            url="http://localhost:8989/add",
            json={
                "product_url": "https://www.wb.ru",
                "user_id": "22222",
            } 
        )

        # check succeed BOT responce
        self.assertEqual(respose.status_code, 200)
        self.assertEqual(
            respose.json(),
            {
                "url": "https://www.wb.ru",
                "user_id": 22222,
                "bot_send_message_text": "successfully added new product to database",
                "bot_reply_to_text": ""
            }
        )

        # chat that second product was actually added to DATABASE
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][0], "https://www.wb.ru")
        self.assertEqual(rows[0][1], "mock_title")
        self.assertEqual(rows[0][2], "mock_vendor")
        self.assertEqual(rows[0][3], "11111")
        # -------------------------------------------------------- #
        self.assertEqual(rows[1][0], "https://www.wb.ru")
        self.assertEqual(rows[1][1], "mock_title")
        self.assertEqual(rows[1][2], "mock_vendor")
        self.assertEqual(rows[1][3], "22222")

        # cleanup environment for other tests
        bot_shutdown()
        postgres_shutdown()

    def test_not_wb_url(self):
        # startup BOT and DATABASE
        postgres_startup()
        bot_startup()

        # wait for BOT and DATABASE environments startup
        time.sleep(env_wait)

        # check that database empty before test
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 0)

        # make HTTP request to BOT to add new product with invalid (not wb) url
        respose = requests.post(
            url="http://localhost:8989/add",
            json={
                "product_url": "https://vk.com",
                "user_id": "55555",
            } 
        )

        # check failed BOT responce
        self.assertEqual(respose.status_code, 400)
        self.assertEqual(
            respose.json(),
            {
                "url": "https://vk.com",
                "user_id": 55555,
                "bot_send_message_text": "",
                "bot_reply_to_text": "failed to add new product: invalid URL (https://vk.com)",
            } 
        )

        # check that product NOT added to DATABASE
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 0)

        # cleanup environment for other tests
        bot_shutdown()
        postgres_shutdown()

    def test_unexisting_url(self):
        # startup BOT and DATABASE
        postgres_startup()
        bot_startup()

        # wait for BOT and DATABASE environments startup
        time.sleep(env_wait)
        
        # check that database empty before test
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 0)

        # make HTTP request to BOT to add new product with invalid (not wb) url
        respose = requests.post(
            url="http://localhost:8989/add",
            json={
                "product_url": "https://some_unknown_url_i_just_imagine.com",
                "user_id": "55555",
            } 
        )

        # check failed BOT responce
        self.assertEqual(respose.status_code, 400)
        self.assertEqual(
            respose.json(),
            {
                "url": "https://some_unknown_url_i_just_imagine.com",
                "user_id": 55555,
                "bot_send_message_text": "",
                "bot_reply_to_text": "failed to add new product: unexisting URL\n(https://some_unknown_url_i_just_imagine.com)",
            } 
        )

        # check that product was not added to DATABASE
        rows = select_from_products(pgdsn=self.pgdsn)
        self.assertEqual(len(rows), 0)

        # cleanup environment for other tests
        bot_shutdown()
        postgres_shutdown()
    
    def test_add_without_database_available(self):
        # startup only BOT
        bot_startup()

        # wait for BOT startup
        time.sleep(env_wait)

        # check that DATABASE actually not avaliable
        with self.assertRaises(Exception) as ex:
            with psycopg2.connect(self.pgdsn) as conn:
                pass


        # make HTTP request to BOT to add new product
        respose = requests.post(
            url="http://localhost:8989/add",
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
                "url": "https://www.wb.ru",
                "user_id": 55555,
                "bot_send_message_text": "",
                "bot_reply_to_text": "failed to add new product: database error",
            } 
        )

        # cleanup environment for other tests
        bot_shutdown()
