import unittest

from model import model
from .telegram import make_user, list_entries


class TestPlatform(unittest.TestCase):

    def test_make_user1(self):
        telegramID = 12345

        user = make_user(user_id=telegramID)

        self.assertEqual(
            user,
            model.User(telegramID=str(telegramID)),
        ) 

    def test_make_user2(self):
        telegramID = 0

        user = make_user(user_id=telegramID)

        self.assertEqual(
            user,
            model.User(telegramID=str(telegramID)), 
        )

    def test_make_user3(self):
        telegramID = 'string'

        user = make_user(user_id=telegramID)

        self.assertEqual(
            user,
            model.User(telegramID=str(telegramID)),
        )

    def test_make_user4(self):
        telegramID = None

        user = make_user(user_id=telegramID)

        self.assertEqual(
            user,
            model.User(telegramID=str(telegramID)),
        )

    def test_list_entries1(self):
        user_entry_1 = model.Entry(
            product=model.Product(
                url="http://myurl1.ru",
                title="mytitle1",
                vendor="myvendor1",
            ),
            user=model.User(
                telegramID="12345",
            ),
        )

        user_entry_2 = model.Entry(
            product=model.Product(
                url="http://myurl2.ru",
                title="mytitle2",
                vendor="myvendor2",
            ),
            user=model.User(
                telegramID="12345",
            ),
        )

        not_user_entry = model.Entry(
            product=model.Product(
                url="http://myurl3.ru",
                title="mytitle3",
                vendor="myvendor3",
            ),
            user=model.User(
                telegramID="54321",
            ),
        )

        user_list = list_entries(
            entry_list=[
                user_entry_1, user_entry_2, not_user_entry,
            ],
            user_id=12345,
        )

        self.assertEqual(len(user_list), 2)
        self.assertEqual(user_list[0], user_entry_1)
        self.assertEqual(user_list[1], user_entry_2)
    
    def test_list_entries2(self):
        user_entry_1 = model.Entry(
            product=model.Product(
                url="http://myurl1.ru",
                title="mytitle1",
                vendor="myvendor1",
            ),
            user=model.User(
                telegramID="12345",
            ),
        )

        not_user_entry = model.Entry(
            product=model.Product(
                url="http://myurl3.ru",
                title="mytitle3",
                vendor="myvendor3",
            ),
            user=model.User(
                telegramID="54321",
            ),
        )

        user_list = list_entries(
            entry_list=[
                user_entry_1, not_user_entry,
            ],
            user_id=12345,
        )

        self.assertEqual(len(user_list), 1)
        self.assertEqual(user_list[0], user_entry_1)

    def test_list_entries3(self):
        not_user_entry = model.Entry(
            product=model.Product(
                url="http://myurl3.ru",
                title="mytitle3",
                vendor="myvendor3",
            ),
            user=model.User(
                telegramID="54321",
            ),
        )

        user_list = list_entries(
            entry_list=[
                not_user_entry,
            ],
            user_id=12345,
        )

        self.assertEqual(len(user_list), 0)
    
    def test_list_entries4(self):
        user_list = list_entries(
            entry_list=[],
            user_id=None,
        )

        self.assertEqual(len(user_list), 0)
