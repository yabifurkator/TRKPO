from model import model


LINES = '----------------------'


class Product:
    def __init__(self, product: model.Product):
        self.product = product 

    def __str__(self) -> str:
        return (
            f"Product:"
            f"\n - url: {self.product.url}"
            f"\n - title: {self.product.title}"
            f"\n - vendor: {self.product.vendor}"
        )
    

class User:
    def __init__(self, user: model.User):
        self.user = user

    def __str__(self) -> str:
        return (
            f"User:"
            f"\n - telegramID: {self.user.telegramID}"
        )
    

class Entry:
    def __init__(self, entry: model.Entry):
        self.entry = entry

    def __str__(self) -> str:
        return (
            f"{LINES}"
            f"\n"
            f"{Product(product=self.entry.product)}"
            f"\n"
            f"{User(user=self.entry.user)}"
            f"\n"
            f"{LINES}"
        )


class ProductWithPrice:
    def __init__(self, product: model.Product, price: model.Price):
        self.product = product
        self.price = price

    def __str__(self) -> str:
        return (
            f"{Product(product=self.product)}"
            f"\n - price: {self.price.value}"
        )
