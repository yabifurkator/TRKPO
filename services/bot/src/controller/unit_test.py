import os
import unittest
from unittest import mock

from model import model
from tools.mock import LoggerMock
from .add import add_controller, add_controller_callback
from .delete import delete_controller, delete_controller_callback
from .getprices import getprices_controller
from .list import list_controller


class TestController(unittest.TestCase):
    @classmethod
    def setUp(self):
        os.environ['POSTGRES_USER'] = 'user'
        os.environ['POSTGRES_PASSWORD'] = 'password'
        os.environ['POSTGRES_DB'] = 'database'

    def test_add_controller(self):
        bot_reply_to_mock = mock.MagicMock('bot_relpy_to_mock')
        bot_mock = mock.MagicMock(name='bot_mock')
        bot_mock.reply_to.return_value = bot_reply_to_mock
        message_mock = mock.MagicMock(name='message_mock')
        logger_mock = LoggerMock()

        add_controller(bot=bot_mock, message=message_mock, logger=logger_mock)

        bot_mock.reply_to.assert_called_once_with(
            message=message_mock,
            text="please, send me a link to the product ↓",
        )
        bot_mock.register_next_step_handler.assert_called_once_with(
            message=bot_reply_to_mock,
            callback=add_controller_callback,
            bot=bot_mock,
            logger=logger_mock,
        )

    @mock.patch('provider.web.wildberries.get_price')
    @mock.patch('provider.platform.telegram.list_entries')
    @mock.patch('provider.database.postgresql.list_entries')
    def test_getprices_controller1(
        self,
        mock_postgresql_list_entries,
        mock_telegram_list_entries,
        mock_wildberries_get_price,
    ):
        entrys = [
            model.Entry(
                product=model.Product(
                    url="http://myurl1.ru",
                    title="mytitle1",
                    vendor="myvendor1",
                ),
                user=model.User(
                    telegramID="12345",
                ),
            ),
            model.Entry(
                product=model.Product(
                    url="http://myurl2.ru",
                    title="mytitle2",
                    vendor="myvendor2",
                ),
                user=model.User(
                    telegramID="12345",
                ),
            ),
            model.Entry(
                product=model.Product(
                    url="http://myurl3.ru",
                    title="mytitle3",
                    vendor="myvendor3",
                ),
                user=model.User(
                    telegramID="12345",
                ),
            )
        ]
    
        mock_postgresql_list_entries.return_value = entrys
        mock_telegram_list_entries.return_value = entrys

        mock_wildberries_get_price.return_value = model.Price(value='999')

        bot_mock = mock.MagicMock(name='bot_mock')
        message_mock = mock.MagicMock(name='message_mock')

        _ = getprices_controller(bot=bot_mock, message=message_mock, logger=mock.MagicMock())

        bot_mock.reply_to.assert_called_once_with(
            message=message_mock,
            text=(
                'prices:\n----------------------\n'
                'Product:\n - url: http://myurl1.ru\n - title: mytitle1\n - vendor: myvendor1\n - price: 999'
                '\n----------------------\n'
                'Product:\n - url: http://myurl2.ru\n - title: mytitle2\n - vendor: myvendor2\n - price: 999'
                '\n----------------------\n'
                'Product:\n - url: http://myurl3.ru\n - title: mytitle3\n - vendor: myvendor3\n - price: 999'
                '\n----------------------'
            ),
        )

    @mock.patch('provider.web.wildberries.get_price')
    @mock.patch('provider.platform.telegram.list_entries')
    @mock.patch('provider.database.postgresql.list_entries')
    def test_getprices_controller2(
        self,
        mock_postgresql_list_entries,
        mock_telegram_list_entries,
        mock_wildberries_get_price,
    ):
        entrys = []
    
        mock_postgresql_list_entries.return_value = entrys
        mock_telegram_list_entries.return_value = entrys

        mock_wildberries_get_price.return_value = model.Price(value='999')

        bot_mock = mock.MagicMock(name='bot_mock')
        message_mock = mock.MagicMock(name='message_mock')

        _ = getprices_controller(bot=bot_mock, message=message_mock, logger=mock.MagicMock())

        bot_mock.reply_to.assert_called_once_with(
            message=message_mock,
            text='prices:\n----------------------',
        )
    
    @mock.patch('provider.web.wildberries.get_price')
    @mock.patch('provider.platform.telegram.list_entries')
    @mock.patch('provider.database.postgresql.list_entries')
    def test_getprices_controller3(
        self,
        mock_postgresql_list_entries,
        mock_telegram_list_entries,
        mock_wildberries_get_price,
    ):
        entrys = [
            model.Entry(
                product=model.Product(
                    url="http://myurl1.ru",
                    title="mytitle1",
                    vendor="myvendor1",
                ),
                user=model.User(
                    telegramID="12345",
                ),
            ),
            model.Entry(
                product=model.Product(
                    url="http://myurl2.ru",
                    title="mytitle2",
                    vendor="myvendor2",
                ),
                user=model.User(
                    telegramID="12345",
                ),
            ),
        ]
    
        mock_postgresql_list_entries.return_value = entrys
        mock_telegram_list_entries.return_value = entrys

        mock_wildberries_get_price.return_value = model.Price(value='999')

        bot_mock = mock.MagicMock(name='bot_mock')
        message_mock = mock.MagicMock(name='message_mock')

        _ = getprices_controller(bot=bot_mock, message=message_mock, logger=mock.MagicMock())

        bot_mock.reply_to.assert_called_once_with(
            message=message_mock,
            text=(
                'prices:\n----------------------\n'
                'Product:\n - url: http://myurl1.ru\n - title: mytitle1\n - vendor: myvendor1\n - price: 999'
                '\n----------------------\n'
                'Product:\n - url: http://myurl2.ru\n - title: mytitle2\n - vendor: myvendor2\n - price: 999'
                '\n----------------------'
            ),
        )

    @mock.patch('provider.web.wildberries.get_price')
    @mock.patch('provider.platform.telegram.list_entries')
    @mock.patch('provider.database.postgresql.list_entries')
    def test_getprices_controller4(
        self,
        mock_postgresql_list_entries,
        mock_telegram_list_entries,
        mock_wildberries_get_price,
    ):
        entrys = [
            model.Entry(
                product=model.Product(
                    url="http://myurl1.ru",
                    title="mytitle1",
                    vendor="myvendor1",
                ),
                user=model.User(
                    telegramID="12345",
                ),
            ),
        ]
    
        mock_postgresql_list_entries.return_value = entrys
        mock_telegram_list_entries.return_value = entrys

        mock_wildberries_get_price.return_value = model.Price(value='999')

        bot_mock = mock.MagicMock(name='bot_mock')
        message_mock = mock.MagicMock(name='message_mock')

        _ = getprices_controller(bot=bot_mock, message=message_mock, logger=mock.MagicMock())

        bot_mock.reply_to.assert_called_once_with(
            message=message_mock,
            text=(
                'prices:\n----------------------\n'
                'Product:\n - url: http://myurl1.ru\n - title: mytitle1\n - vendor: myvendor1\n - price: 999'
                '\n----------------------'
            ),
        )

    @mock.patch('provider.platform.telegram.list_entries')
    @mock.patch('provider.database.postgresql.list_entries')
    def test_list_controller1(
        self,
        mock_postgresql_list_entries,
        mock_telegram_list_entries,
    ):
        entrys = [
            model.Entry(
                product=model.Product(
                    url="http://myurl1.ru",
                    title="mytitle1",
                    vendor="myvendor1",
                ),
                user=model.User(
                    telegramID="12345",
                ),
            ),
            model.Entry(
                product=model.Product(
                    url="http://myurl2.ru",
                    title="mytitle2",
                    vendor="myvendor2",
                ),
                user=model.User(
                    telegramID="12345",
                ),
            ),
            model.Entry(
                product=model.Product(
                    url="http://myurl3.ru",
                    title="mytitle3",
                    vendor="myvendor3",
                ),
                user=model.User(
                    telegramID="12345",
                ),
            )
        ]
    
        mock_postgresql_list_entries.return_value = entrys
        mock_telegram_list_entries.return_value = entrys
        
        bot_mock = mock.MagicMock(name='bot_mock')
        message_mock = mock.MagicMock(name='message_mock')

        _ = list_controller(bot=bot_mock, message=message_mock, logger=mock.MagicMock())

        bot_mock.reply_to.assert_called_once_with(
            message=message_mock,
            text=(
                'products:\n----------------------\n'
                'Product:\n - url: http://myurl1.ru\n - title: mytitle1\n - vendor: myvendor1'
                '\n----------------------\n'
                'Product:\n - url: http://myurl2.ru\n - title: mytitle2\n - vendor: myvendor2'
                '\n----------------------\n'
                'Product:\n - url: http://myurl3.ru\n - title: mytitle3\n - vendor: myvendor3'
                '\n----------------------'
            )
        )
    
    @mock.patch('provider.platform.telegram.list_entries')
    @mock.patch('provider.database.postgresql.list_entries')
    def test_list_controller2(
        self,
        mock_postgresql_list_entries,
        mock_telegram_list_entries,
    ):
        entrys = [
            model.Entry(
                product=model.Product(
                    url="http://myurl1.ru",
                    title="mytitle1",
                    vendor="myvendor1",
                ),
                user=model.User(
                    telegramID="12345",
                ),
            ),
            model.Entry(
                product=model.Product(
                    url="http://myurl2.ru",
                    title="mytitle2",
                    vendor="myvendor2",
                ),
                user=model.User(
                    telegramID="12345",
                ),
            ),
        ]
    
        mock_postgresql_list_entries.return_value = entrys
        mock_telegram_list_entries.return_value = entrys
        
        bot_mock = mock.MagicMock(name='bot_mock')
        message_mock = mock.MagicMock(name='message_mock')

        _ = list_controller(bot=bot_mock, message=message_mock, logger=mock.MagicMock())

        bot_mock.reply_to.assert_called_once_with(
            message=message_mock,
            text=(
                'products:\n----------------------\n'
                'Product:\n - url: http://myurl1.ru\n - title: mytitle1\n - vendor: myvendor1'
                '\n----------------------\n'
                'Product:\n - url: http://myurl2.ru\n - title: mytitle2\n - vendor: myvendor2'
                '\n----------------------'
            )
        )

    @mock.patch('provider.platform.telegram.list_entries')
    @mock.patch('provider.database.postgresql.list_entries')
    def test_list_controller3(
        self,
        mock_postgresql_list_entries,
        mock_telegram_list_entries,
    ):
        entrys = [
            model.Entry(
                product=model.Product(
                    url="http://myurl1.ru",
                    title="mytitle1",
                    vendor="myvendor1",
                ),
                user=model.User(
                    telegramID="12345",
                ),
            ),
        ]
    
        mock_postgresql_list_entries.return_value = entrys
        mock_telegram_list_entries.return_value = entrys
        
        bot_mock = mock.MagicMock(name='bot_mock')
        message_mock = mock.MagicMock(name='message_mock')

        _ = list_controller(bot=bot_mock, message=message_mock, logger=mock.MagicMock())

        bot_mock.reply_to.assert_called_once_with(
            message=message_mock,
            text=(
                'products:\n----------------------\n'
                'Product:\n - url: http://myurl1.ru\n - title: mytitle1\n - vendor: myvendor1'
                '\n----------------------'
            )
        )

    @mock.patch('provider.platform.telegram.list_entries')
    @mock.patch('provider.database.postgresql.list_entries')
    def test_list_controller_empty(
        self,
        mock_postgresql_list_entries,
        mock_telegram_list_entries,
    ):
        entrys = []
    
        mock_postgresql_list_entries.return_value = entrys
        mock_telegram_list_entries.return_value = entrys
        
        bot_mock = mock.MagicMock(name='bot_mock')
        message_mock = mock.MagicMock(name='message_mock')

        _ = list_controller(bot=bot_mock, message=message_mock, logger=mock.MagicMock())

        bot_mock.reply_to.assert_called_once_with(
            message=message_mock,
            text=(
                'products:'
                '\n----------------------\n'
                'not found'
            )
        )
