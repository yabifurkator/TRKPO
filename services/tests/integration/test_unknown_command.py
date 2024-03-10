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
    env_wait


class TestUnknownCommand(unittest.TestCase):
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

    def test_unknown_command(self):
        # startup BOT and DATABASE
        postgres_startup()
        bot_startup()

        # wait for BOT and DATABASE environments startup
        time.sleep(env_wait)

        # make HTTP request to BOT with unknown command
        respose = requests.get(url="http://localhost:8989/random_unexistins_command")

        # check succeed BOT responce
        self.assertEqual(respose.status_code, 404)
        self.assertEqual(
            respose.json(),
            {
                "command": "not found",
            } 
        )

        # cleanup environment for other tests
        bot_shutdown()
        postgres_shutdown()
