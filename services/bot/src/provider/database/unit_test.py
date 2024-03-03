import pytest
import unittest
from unittest import mock
import os

from psycopg2.errors import UniqueViolation

from model import model
from tools.mock import LoggerMock
from .postgresql import make_entry, insert_entry, list_entries, delete_entry
from .exceptions import AlreadyExistsException, NotFoundException


class TestExceptions(unittest.TestCase):
    def test_already_exists_message(self):
        exception = AlreadyExistsException()
        self.assertEqual(str(exception), "already exists")

    def test_not_found_message(self):
        exception = NotFoundException()
        self.assertEqual(str(exception), "not found")


class TestPostgresql(unittest.TestCase):
    @classmethod
    def setUp(self):
        os.environ['POSTGRES_USER'] = 'user'
        os.environ['POSTGRES_PASSWORD'] = 'password'
        os.environ['POSTGRES_DB'] = 'database'

    def test_make_entry1(self):
        product=model.Product(
            url="http://myurl.ru",
            title="mytitle",
            vendor="myvendor",
        )
        
        user=model.User(
                telegramID="12345",
        )

        entry = make_entry(
            product=product,
            user=user,
        )

        self.assertEqual(entry.product, product)
        self.assertEqual(entry.user, user)
    
    def test_make_entry2(self):
        product=model.Product(
            url="notvalidurl",
            title="sometitle",
            vendor="somevendor",
        )
        
        user=model.User(
                telegramID="notvalidid",
        )

        entry = make_entry(
            product=product,
            user=user,
        )

        self.assertEqual(entry.product, product)
        self.assertEqual(entry.user, user)
    
    def test_make_entry3(self):
        product=model.Product(
            url="htts://unexisting.url.polytech.usa",
            title="goodtitle",
            vendor="goodvendor",
        )
        
        user=model.User(
                telegramID="11223344",
        )

        entry = make_entry(
            product=product,
            user=user,
        )

        self.assertEqual(entry.product, product)
        self.assertEqual(entry.user, user)

    def test_make_entry4(self):
        product=model.Product(
            url="",
            title="",
            vendor="",
        )
        
        user=model.User(
                telegramID="",
        )

        entry = make_entry(
            product=product,
            user=user,
        )

        self.assertEqual(entry.product, product)
        self.assertEqual(entry.user, user)

    @mock.patch('psycopg2.connect')
    def test_delete_entry1(self, mock_connect):
        entry = model.Entry(
            product=model.Product(
                url="http://myurl.ru",
                title="mytitle",
                vendor="myvendor",
            ),
            user=model.User(
                telegramID="12345",
            ),
        )

        _ = delete_entry(
            entry=entry,
            logger=LoggerMock(),
        )

        mock_connect(). \
            __enter__().cursor(). \
            __enter__().execute. \
            assert_called_once_with(
                f"DELETE FROM products "
                f"WHERE url='{entry.product.url}' AND user_telegram_id='{entry.user.telegramID}'"
            )
        
    @mock.patch('psycopg2.connect')
    def test_delete_entry2(self, mock_connect):
        entry = model.Entry(
            product=model.Product(
                url="notvalidurl",
                title="sometitle",
                vendor="somevendor",
            ), 
            user=model.User(
                telegramID="notvalidid",
            ),
        )

        _ = delete_entry(
            entry=entry,
            logger=LoggerMock(),
        )

        mock_connect(). \
            __enter__().cursor(). \
            __enter__().execute. \
            assert_called_once_with(
                f"DELETE FROM products "
                f"WHERE url='{entry.product.url}' AND user_telegram_id='{entry.user.telegramID}'"
            )
        
    @mock.patch('psycopg2.connect')
    def test_delete_entry3(self, mock_connect):
        entry = model.Entry(
            product=model.Product(
                url="htts://unexisting.url.polytech.usa",
                title="goodtitle",
                vendor="goodvendor",
            ), 
            user=model.User(
                    telegramID="11223344",
            ),
        )

        _ = delete_entry(
            entry=entry,
            logger=LoggerMock(),
        )

        mock_connect(). \
            __enter__().cursor(). \
            __enter__().execute. \
            assert_called_once_with(
                f"DELETE FROM products "
                f"WHERE url='{entry.product.url}' AND user_telegram_id='{entry.user.telegramID}'"
            )

    @mock.patch('psycopg2.connect')
    def test_delete_entry4(self, mock_connect):
        entry = model.Entry(
            product=model.Product(
                url="",
                title="",
                vendor="",
            ), 
            user=model.User(
                telegramID="",
            ),
        )

        _ = delete_entry(
            entry=entry,
            logger=LoggerMock(),
        )

        mock_connect(). \
            __enter__().cursor(). \
            __enter__().execute. \
            assert_called_once_with(
                f"DELETE FROM products "
                f"WHERE url='{entry.product.url}' AND user_telegram_id='{entry.user.telegramID}'"
            )
        
    @mock.patch('psycopg2.connect')
    def test_delete_entry_exception1(self, mock_connect):
        entry = model.Entry(
            product=model.Product(
                url="http://myurl.ru",
                title="mytitle",
                vendor="myvendor",
            ),
            user=model.User(
                telegramID="12345",
            ),
        ) 

        mock_connect().__enter__().cursor().__enter__().rowcount = 0

        with pytest.raises(NotFoundException) as ex_info:
            _ = delete_entry(
                entry=entry,
                logger=LoggerMock(),
            )
        
        self.assertEqual(str(ex_info.value), str(NotFoundException()))
    
    @mock.patch('psycopg2.connect')
    def test_delete_entry_exception2(self, mock_connect):
        entry = model.Entry(
            product=model.Product(
                url="notvalidurl",
                title="sometitle",
                vendor="somevendor",
            ), 
            user=model.User(
                telegramID="notvalidid",
            ),
        )

        mock_connect().__enter__().cursor().__enter__().rowcount = 0

        with pytest.raises(NotFoundException) as ex_info:
            _ = delete_entry(
                entry=entry,
                logger=LoggerMock(),
            )
        
        self.assertEqual(str(ex_info.value), str(NotFoundException()))
    
    @mock.patch('psycopg2.connect')
    def test_delete_entry_exception3(self, mock_connect):
        entry = model.Entry(
            product=model.Product(
                url="htts://unexisting.url.polytech.usa",
                title="goodtitle",
                vendor="goodvendor",
            ), 
            user=model.User(
                    telegramID="11223344",
            ),
        )

        mock_connect().__enter__().cursor().__enter__().rowcount = 0

        with pytest.raises(NotFoundException) as ex_info:
            _ = delete_entry(
                entry=entry,
                logger=LoggerMock(),
            )
        
        self.assertEqual(str(ex_info.value), str(NotFoundException()))

    @mock.patch('psycopg2.connect')
    def test_delete_entry_exception4(self, mock_connect):
        entry = model.Entry(
            product=model.Product(
                url="",
                title="",
                vendor="",
            ), 
            user=model.User(
                telegramID="",
            ),
        )

        mock_connect().__enter__().cursor().__enter__().rowcount = 0

        with pytest.raises(NotFoundException) as ex_info:
            _ = delete_entry(
                entry=entry,
                logger=LoggerMock(),
            )
        
        self.assertEqual(str(ex_info.value), str(NotFoundException()))

    @mock.patch('psycopg2.connect')
    def test_list_entries(self, mock_connect): 
        mock_connect(). \
            __enter__().cursor(). \
            __enter__().fetchall.return_value = [
                ["http://url1.ru", "mytitle1", "myvendor1", "myid1"],
                ["http://url2.ru", "mytitle2", "myvendor2", "myid2"],
            ]
         
        result = list_entries(logger=LoggerMock())

        self.assertEqual(result[0], model.Entry(
            product=model.Product(
                url="http://url1.ru",
                title="mytitle1",
                vendor="myvendor1",
            ),
            user=model.User(
                telegramID="myid1",
            ),
        ))

        self.assertEqual(result[1], model.Entry(
            product=model.Product(
                url="http://url2.ru",
                title="mytitle2",
                vendor="myvendor2",
            ),
            user=model.User(
                telegramID="myid2",
            ),
        ))

    @mock.patch('psycopg2.connect')
    def test_list_entries_more(self, mock_connect): 
        mock_connect(). \
            __enter__().cursor(). \
            __enter__().fetchall.return_value = [
                ["http://url1.ru", "mytitle1", "myvendor1", "myid1"],
                ["http://url2.ru", "mytitle2", "myvendor2", "myid2"],
                ["http://url3.ru", "mytitle3", "myvendor3", "myid3"],
            ]
         
        result = list_entries(logger=LoggerMock())

        self.assertEqual(result[0], model.Entry(
            product=model.Product(
                url="http://url1.ru",
                title="mytitle1",
                vendor="myvendor1",
            ),
            user=model.User(
                telegramID="myid1",
            ),
        ))

        self.assertEqual(result[1], model.Entry(
            product=model.Product(
                url="http://url2.ru",
                title="mytitle2",
                vendor="myvendor2",
            ),
            user=model.User(
                telegramID="myid2",
            ),
        ))

        self.assertEqual(result[2], model.Entry(
            product=model.Product(
                url="http://url3.ru",
                title="mytitle3",
                vendor="myvendor3",
            ),
            user=model.User(
                telegramID="myid3",
            ),
        ))

    @mock.patch('psycopg2.connect')
    def test_list_entries_empty(self, mock_connect): 
        mock_connect(). \
            __enter__().cursor(). \
            __enter__().fetchall.return_value = []
         
        result = list_entries(logger=LoggerMock())

        self.assertEqual(len(result), 0)

    @mock.patch('psycopg2.connect')
    def test_list_entries_not_valid(self, mock_connect): 
        mock_connect(). \
            __enter__().cursor(). \
            __enter__().fetchall.return_value = [
                [],
                [],
            ]

        with pytest.raises(IndexError):
            _ = list_entries(logger=LoggerMock())

    @mock.patch('psycopg2.connect')
    def test_list_entries_not_valid_none(self, mock_connect): 
        mock_connect(). \
            __enter__().cursor(). \
            __enter__().fetchall.return_value = None

        with pytest.raises(TypeError):
            _ = list_entries(logger=LoggerMock())
        
    @mock.patch('psycopg2.connect')
    def test_insert_entry1(self, mock_connect):
        entry = model.Entry(
            product=model.Product(
                url="http://myurl.ru",
                title="mytitle",
                vendor="myvendor",
            ),
            user=model.User(
                telegramID="12345",
            ),
        )

        _ = insert_entry(
            entry=entry,
            logger=LoggerMock(),
        )

        mock_connect(). \
            __enter__().cursor(). \
            __enter__().execute. \
            assert_called_once_with(
                f"INSERT INTO products "
                f"(url, title, vendor, user_telegram_id) VALUES "
                f"('{entry.product.url}', '{entry.product.title}', '{entry.product.vendor}', '{entry.user.telegramID}')"
            )

    @mock.patch('psycopg2.connect')
    def test_insert_entry2(self, mock_connect):
        entry = model.Entry(
            product=model.Product(
                url="notvalidurl",
                title="sometitle",
                vendor="somevendor",
            ), 
            user=model.User(
                telegramID="notvalidid",
            ),
        )

        _ = insert_entry(
            entry=entry,
            logger=LoggerMock(),
        )

        mock_connect(). \
            __enter__().cursor(). \
            __enter__().execute. \
            assert_called_once_with(
                f"INSERT INTO products "
                f"(url, title, vendor, user_telegram_id) VALUES "
                f"('{entry.product.url}', '{entry.product.title}', '{entry.product.vendor}', '{entry.user.telegramID}')"
            )
        
    @mock.patch('psycopg2.connect')
    def test_insert_entry3(self, mock_connect):
        entry = model.Entry(
            product=model.Product(
                url="htts://unexisting.url.polytech.usa",
                title="goodtitle",
                vendor="goodvendor",
            ), 
            user=model.User(
                telegramID="11223344",
            ),
        )

        _ = insert_entry(
            entry=entry,
            logger=LoggerMock(),
        )

        mock_connect(). \
            __enter__().cursor(). \
            __enter__().execute. \
            assert_called_once_with(
                f"INSERT INTO products "
                f"(url, title, vendor, user_telegram_id) VALUES "
                f"('{entry.product.url}', '{entry.product.title}', '{entry.product.vendor}', '{entry.user.telegramID}')"
            )
        
    @mock.patch('psycopg2.connect')
    def test_insert_entry4(self, mock_connect):
        entry = model.Entry(
            product=model.Product(
                url="",
                title="",
                vendor="",
            ), 
            user=model.User(
                telegramID="",
            ),
        )

        _ = insert_entry(
            entry=entry,
            logger=LoggerMock(),
        )

        mock_connect(). \
            __enter__().cursor(). \
            __enter__().execute. \
            assert_called_once_with(
                f"INSERT INTO products "
                f"(url, title, vendor, user_telegram_id) VALUES "
                f"('{entry.product.url}', '{entry.product.title}', '{entry.product.vendor}', '{entry.user.telegramID}')"
            )

    @mock.patch('psycopg2.connect', side_effect=UniqueViolation)
    def test_insert_entry_exception1(self, mock_connect):
        with pytest.raises(AlreadyExistsException) as ex_info:
            _ = insert_entry(
                entry = model.Entry(
                    product=model.Product(
                        url="notvalidurl",
                        title="sometitle",
                        vendor="somevendor",
                    ), 
                    user=model.User(
                        telegramID="notvalidid",
                    ),
                ),
                logger=LoggerMock(),
            )

        self.assertEqual(str(ex_info.value), str(AlreadyExistsException()))

    @mock.patch('psycopg2.connect', side_effect=UniqueViolation)
    def test_insert_entry_exception2(self, mock_connect):
        with pytest.raises(AlreadyExistsException) as ex_info:
            _ = insert_entry(
                entry=model.Entry(
                    product=model.Product(
                        url="http://myurl.ru",
                        title="mytitle",
                        vendor="myvendor",
                    ),
                    user=model.User(
                        telegramID="12345",
                    ),
                ),
                logger=LoggerMock(),
            )

        self.assertEqual(str(ex_info.value), str(AlreadyExistsException()))

    @mock.patch('psycopg2.connect', side_effect=UniqueViolation)
    def test_insert_entry_exception3(self, mock_connect):
        with pytest.raises(AlreadyExistsException) as ex_info:
            _ = insert_entry(
                entry = model.Entry(
                    product=model.Product(
                        url="htts://unexisting.url.polytech.usa",
                        title="goodtitle",
                        vendor="goodvendor",
                    ), 
                    user=model.User(
                            telegramID="11223344",
                    ),
                ),
                logger=LoggerMock(),
            )

        self.assertEqual(str(ex_info.value), str(AlreadyExistsException()))
    
    @mock.patch('psycopg2.connect', side_effect=UniqueViolation)
    def test_insert_entry_exception4(self, mock_connect):
        with pytest.raises(AlreadyExistsException) as ex_info:
            _ = insert_entry(
                entry = model.Entry(
                    product=model.Product(
                        url="",
                        title="",
                        vendor="",
                    ), 
                    user=model.User(
                        telegramID="",
                    ),
                ),
                logger=LoggerMock(),
            )

        self.assertEqual(str(ex_info.value), str(AlreadyExistsException()))
