from dataclasses import dataclass


@dataclass
class Product:
    url: str
    title: str
    vendor: str


@dataclass
class User:
    telegramID: str


@dataclass
class Entry:
    product: Product
    user: User


@dataclass
class Price:
    value: str
