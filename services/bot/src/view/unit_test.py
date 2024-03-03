import unittest

from model import model
from view.view import Product, User, Entry, ProductWithPrice, LINES

class TestView(unittest.TestCase):

    def test_product_view1(self):
        product_view = Product(
            product=model.Product(
                url="http://myurl.ru",
                title="sometitle",
                vendor="somevendor",
            )
        )

        self.assertEqual(
            str(product_view),
            (
                f"Product:"
                f"\n - url: {product_view.product.url}"
                f"\n - title: {product_view.product.title}"
                f"\n - vendor: {product_view.product.vendor}"
            )
        )
    
    def test_product_view2(self):
        product_view = Product(
            product=model.Product(
                url="notvalidurl",
                title="sometitle",
                vendor="somevendor",
            ), 
        )

        self.assertEqual(
            str(product_view),
            (
                f"Product:"
                f"\n - url: {product_view.product.url}"
                f"\n - title: {product_view.product.title}"
                f"\n - vendor: {product_view.product.vendor}"
            )
        )

    def test_product_view3(self):
        product_view = Product(
            product=model.Product(
                url="htts://unexisting.url.polytech.usa",
                title="goodtitle",
                vendor="goodvendor",
            ),
        )

        self.assertEqual(
            str(product_view),
            (
                f"Product:"
                f"\n - url: {product_view.product.url}"
                f"\n - title: {product_view.product.title}"
                f"\n - vendor: {product_view.product.vendor}"
            )
        )

    def test_user_view1(self):
        user_view = User(
            user=model.User(
                telegramID='12345',
            ),
        )

        self.assertEqual(
            str(user_view),
            (
                f"User:"
                f"\n - telegramID: {user_view.user.telegramID}"
            )
        )

    def test_user_view2(self):
        user_view = User(
            user=model.User(
                telegramID=12345,
            ),
        )

        self.assertEqual(
            str(user_view),
            (
                f"User:"
                f"\n - telegramID: {user_view.user.telegramID}"
            )
        )

    def test_user_view3(self):
        user_view = User(
            user=model.User(
                telegramID='string',
            ),
        )

        self.assertEqual(
            str(user_view),
            (
                f"User:"
                f"\n - telegramID: {user_view.user.telegramID}"
            )
        )

    def test_entry_view1(self):
        entry_view = Entry(
            entry=model.Entry(
                product=model.Product(
                    url="http://myurl.ru",
                    title="sometitle",
                    vendor="somevendor",
                ),
                user=model.User(
                    telegramID='12345',
                ),
            )
        )

        self.assertEqual(
            str(entry_view),
            (
                f"{LINES}"
                f"\n"
                f"{Product(product=entry_view.entry.product)}"
                f"\n"
                f"{User(entry_view.entry.user)}"
                f"\n"
                f"{LINES}"
            )
        )

    def test_entry_view2(self):
        entry_view = Entry(
            entry=model.Entry(
                product=model.Product(
                    url="notvalidurl",
                    title="sometitle",
                    vendor="somevendor",
                ), 
                user=model.User(
                    telegramID='12345',
                ),
            )
        )

        self.assertEqual(
            str(entry_view),
            (
                f"{LINES}"
                f"\n"
                f"{Product(product=entry_view.entry.product)}"
                f"\n"
                f"{User(entry_view.entry.user)}"
                f"\n"
                f"{LINES}"
            )
        )

    def test_entry_view3(self):
        entry_view = Entry(
            entry=model.Entry(
                product=model.Product(
                    url="notvalidurl",
                    title="sometitle",
                    vendor="somevendor",
                ), 
                user=model.User(
                    telegramID='12345',
                ),
            )
        )

        self.assertEqual(
            str(entry_view),
            (
                f"{LINES}"
                f"\n"
                f"{Product(product=entry_view.entry.product)}"
                f"\n"
                f"{User(entry_view.entry.user)}"
                f"\n"
                f"{LINES}"
            )
        )

    def test_product_with_price_view1(self):
        product_with_price_view = ProductWithPrice(
            product=model.Product(
                url="htts://unexisting.url.polytech.usa",
                title="goodtitle",
                vendor="goodvendor",
            ),
            price=model.Price(value="999")
        )

        self.assertEqual(
            str(product_with_price_view),
            (
                f"{Product(product=product_with_price_view.product)}"
                f"\n - price: {product_with_price_view.price.value}"
            )
        )

    def test_product_with_price_view2(self):
        product_with_price_view = ProductWithPrice(
            product=model.Product(
                url="notvalidurl",
                title="sometitle",
                vendor="somevendor",
            ), 
            price=model.Price(value="999")
        )

        self.assertEqual(
            str(product_with_price_view),
            (
                f"{Product(product=product_with_price_view.product)}"
                f"\n - price: {product_with_price_view.price.value}"
            )
        )
    
    def test_product_with_price_view3(self):
        product_with_price_view = ProductWithPrice(
            product=model.Product(
                url="http://myurl.ru",
                title="sometitle",
                vendor="somevendor",
            ),
            price=model.Price(value="999")
        )

        self.assertEqual(
            str(product_with_price_view),
            (
                f"{Product(product=product_with_price_view.product)}"
                f"\n - price: {product_with_price_view.price.value}"
            )
        )


