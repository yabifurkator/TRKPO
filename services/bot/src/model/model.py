from dataclasses import dataclass


@dataclass
class Product:
    url: str
    title: str
    vendor: str

    def get_url(self) -> str:
        return self.url

    def get_title(self) -> str:
        return self.title

    def get_vendor(self) -> str:
        return self.vendor


@dataclass
class User:
    telegramID: str

    def get_telegramID(self) -> str:
        return self.telegramID


@dataclass
class Entry:
    product: Product
    user: User

    def get_product(self) -> str:
        return self.product
    
    def get_user(self) -> str:
        return self.user
    
    def get_title(self) -> str:
        return self.product.title
    
    def get_vendor(self) -> str:
        return self.product.vendor


@dataclass
class Price:
    value: str

    def get_value(self) -> str:
        return self.value
