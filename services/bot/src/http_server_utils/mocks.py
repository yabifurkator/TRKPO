import logging

from model import model
from provider.web.exceptions import InvalidUrlException

class UserReplyMock:
    class FromUser:
        def __init__(self, user_id: int):
            self.id = user_id

    class Chat:
        def __init__(self):
            self.id = 456

    def __init__(self, url: str, user_id: int):
        self.text = url
        self.from_user = UserReplyMock.FromUser(user_id=user_id)
        self.chat = UserReplyMock.Chat()


class MessageMock:
    def __init__(self, user_id: int):
        self.from_user = UserReplyMock.FromUser(user_id=user_id)
        self.chat = UserReplyMock.Chat()


class BotMock:
    def __init__(self):
        self.send_message_text = ""
        self.reply_to_text = ""

    def reply_to(self, message: UserReplyMock, text: str):
        self.message = message
        self.reply_to_text = text
    
    def send_message(self, chat_id: int, text: str):
        self.chat_id = chat_id
        self.send_message_text = text


from provider.web.exceptions import InvalidUrlException, UnexistingUrlException

def wildberries_make_product_mock(url: str, no_parse=False) -> model.Product:
    if url == "https://www.wb.ru":
        return model.Product(
            url=url,
            title="mock_title",
            vendor="mock_vendor",
        )
    elif url == "https://vk.com":
        raise InvalidUrlException(url=url)
    else:
        raise UnexistingUrlException(url=url)


def wildberries_get_price_mock(product: model.Product, logger: logging.Logger) -> model.Price:
    if product.title == "wildberries_exception":
        raise Exception("unexpected exception on wildberries side")
    if "https://www.wb.ru" in product.url:
        return model.Price(value=999)
    else:
        raise UnexistingUrlException(url=product.url)
