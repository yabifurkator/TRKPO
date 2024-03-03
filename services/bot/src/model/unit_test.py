import pytest
import unittest

from .model import Product, User, Entry, Price

class TestModel(unittest.TestCase):

    def test_product_url(self):
        product = Product(url="url1", title="title1", vendor="vendor1")

        url = product.get_url()
        self.assertEqual(url, "url1")
    
    def test_product_title(self):
        product = Product(url="url1", title="title1", vendor="vendor1")

        title = product.get_title()
        self.assertEqual(title, "title1")

    def test_product_vendor(self):
        product = Product(url="url1", title="title1", vendor="vendor1")

        vendor = product.get_vendor()
        self.assertEqual(vendor, "vendor1")
    
    def test_product_modrl(self):
        product = Product(url="url1", title="title1", vendor="vendor1")
        self.assertEqual("url1", product.url)
        self.assertEqual("title1", product.title)
        self.assertEqual("vendor1", product.vendor)

    def test_user_telegram_id(self):
        user = User(telegramID=1234)

        tid = user.get_telegramID()
        self.assertEqual(tid, 1234)
    
    def test_user_model(self):
        user = User(telegramID=1234)
        self.assertEqual(1234, user.telegramID)

    def test_entry_product(self):
        entry = Entry(
            product=Product(url="url1", title="title1", vendor="vendor1"), user=User(telegramID=1234),
        )

        product = entry.get_product()
        
        self.assertEqual(
            product,
            Product(url="url1", title="title1", vendor="vendor1"),
        )

    def test_entry_user(self):
        entry = Entry(
            product=Product(url="url1", title="title1", vendor="vendor1"), user=User(telegramID=1234),
        )
        self.assertEqual(entry.get_user(), User(telegramID=1234))

    def test_entry_title(self):
        entry = Entry(
            product=Product(url="url1", title="title1", vendor="vendor1"), user=User(telegramID=1234),
        )
        self.assertEqual(entry.get_title(), "title1")
    
    def test_entry_vendor(self):
        entry = Entry(
            product=Product(url="url1", title="title1", vendor="vendor1"), user=User(telegramID=1234),
        )

        self.assertEqual(entry.get_vendor(), "vendor1")

    def test_entry_model(self):
        entry = Entry(
            product=Product(url="url1", title="title1", vendor="vendor1"), user=User(telegramID=1234),
        )

        self.assertEqual(
            entry.product,
            Product(url="url1", title="title1", vendor="vendor1"),
        )
    
    def test_price_value(self):
        price = Price(value="999")

        v = price.get_value()

        self.assertEqual("999", v)

    def test_price_model(self):
        price = Price(value="999")

        self.assertEqual(price.value, "999")
