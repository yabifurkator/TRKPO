import pytest
import unittest
from unittest import mock

from selenium.common.exceptions import InvalidArgumentException, WebDriverException

from model import model
from tools.mock import LoggerMock
from .wildberries import make_product, get_price
from .exceptions import InvalidUrlException, UnexistingUrlException

class TestWeb(unittest.TestCase):

    @mock.patch("selenium.webdriver.support.ui.WebDriverWait.__new__")
    @mock.patch("selenium.webdriver.Chrome.__new__")
    @mock.patch("selenium.webdriver.chrome.service.Service.__new__")
    @mock.patch("webdriver_manager.chrome.ChromeDriverManager.__new__")
    def test_make_product1(
        self,
        mock_chromge_driver_manager_new,
        mock_webdriver_service_new,
        mock_webdriver_chrome_new,
        mock_webdriver_wait_new,
    ):
        chrome_driver_manager_new_mock = mock.MagicMock(name='chrome_driver_manager')
        chrome_driver_manager_new_mock.install.return_value = None
        mock_chromge_driver_manager_new.return_value = chrome_driver_manager_new_mock

        service_mock = mock.MagicMock(name='service')
        mock_webdriver_service_new.return_value = service_mock

        webdriver_chrome_new_mock = mock.MagicMock(name='webdriver_chrome')
        webdriver_chrome_new_mock.get.return_value = None
        mock_webdriver_chrome_new.return_value = webdriver_chrome_new_mock

        webdriver_wait_until_mock = mock.MagicMock(name='webdriver_wait_until')
        webdriver_wait_until_mock.find_element.return_value.text = 'property'

        webdriver_wait_new_mock = mock.MagicMock(name='webdriver_wait')
        webdriver_wait_new_mock.until.return_value = webdriver_wait_until_mock
        mock_webdriver_wait_new.return_value = webdriver_wait_new_mock

        product = make_product(url="http://vk.com")

        self.assertEqual(product.url, "http://vk.com")
        self.assertEqual(product.title, "property")
        self.assertEqual(product.vendor, "property")

    @mock.patch("selenium.webdriver.support.ui.WebDriverWait.__new__")
    @mock.patch("selenium.webdriver.Chrome.__new__")
    @mock.patch("selenium.webdriver.chrome.service.Service.__new__")
    @mock.patch("webdriver_manager.chrome.ChromeDriverManager.__new__")
    def test_make_product2(
        self,
        mock_chromge_driver_manager_new,
        mock_webdriver_service_new,
        mock_webdriver_chrome_new,
        mock_webdriver_wait_new,
    ):
        chrome_driver_manager_new_mock = mock.MagicMock(name='chrome_driver_manager')
        chrome_driver_manager_new_mock.install.return_value = None
        mock_chromge_driver_manager_new.return_value = chrome_driver_manager_new_mock

        service_mock = mock.MagicMock(name='service')
        mock_webdriver_service_new.return_value = service_mock

        webdriver_chrome_new_mock = mock.MagicMock(name='webdriver_chrome')
        webdriver_chrome_new_mock.get.return_value = None
        mock_webdriver_chrome_new.return_value = webdriver_chrome_new_mock

        webdriver_wait_until_mock = mock.MagicMock(name='webdriver_wait_until')
        webdriver_wait_until_mock.find_element.return_value.text = '112233'

        webdriver_wait_new_mock = mock.MagicMock(name='webdriver_wait')
        webdriver_wait_new_mock.until.return_value = webdriver_wait_until_mock
        mock_webdriver_wait_new.return_value = webdriver_wait_new_mock

        product = make_product(url="not_valid_url")

        self.assertEqual(product.url, "not_valid_url")
        self.assertEqual(product.title, "112233")
        self.assertEqual(product.vendor, "112233")

    @mock.patch("selenium.webdriver.support.ui.WebDriverWait.__new__")
    @mock.patch("selenium.webdriver.Chrome.__new__")
    @mock.patch("selenium.webdriver.chrome.service.Service.__new__")
    @mock.patch("webdriver_manager.chrome.ChromeDriverManager.__new__")
    def test_make_product3(
        self,
        mock_chromge_driver_manager_new,
        mock_webdriver_service_new,
        mock_webdriver_chrome_new,
        mock_webdriver_wait_new,
    ):
        chrome_driver_manager_new_mock = mock.MagicMock(name='chrome_driver_manager')
        chrome_driver_manager_new_mock.install.return_value = None
        mock_chromge_driver_manager_new.return_value = chrome_driver_manager_new_mock

        service_mock = mock.MagicMock(name='service')
        mock_webdriver_service_new.return_value = service_mock

        webdriver_chrome_new_mock = mock.MagicMock(name='webdriver_chrome')
        webdriver_chrome_new_mock.get.return_value = None
        mock_webdriver_chrome_new.return_value = webdriver_chrome_new_mock

        webdriver_wait_until_mock = mock.MagicMock(name='webdriver_wait_until')
        webdriver_wait_until_mock.find_element.return_value.text = 'sometext'

        webdriver_wait_new_mock = mock.MagicMock(name='webdriver_wait')
        webdriver_wait_new_mock.until.return_value = webdriver_wait_until_mock
        mock_webdriver_wait_new.return_value = webdriver_wait_new_mock

        product = make_product(url="htts://unexisting.url.polytech.usa")

        self.assertEqual(product.url, "htts://unexisting.url.polytech.usa")
        self.assertEqual(product.title, "sometext")
        self.assertEqual(product.vendor, "sometext")
    
    @mock.patch("webdriver_manager.chrome.ChromeDriverManager.__new__", side_effect=InvalidArgumentException)
    def test_make_product_invalid_url_exception1(self, mock_chromge_driver_manager_new):
        with pytest.raises(InvalidUrlException) as ex_info:
            _ = make_product(url="someurl")

        self.assertEqual(str(ex_info.value), str(InvalidUrlException(url="someurl")))
    
    @mock.patch("webdriver_manager.chrome.ChromeDriverManager.__new__", side_effect=InvalidArgumentException)
    def test_make_product_invalid_url_exception2(self, mock_chromge_driver_manager_new):
        with pytest.raises(InvalidUrlException) as ex_info:
            _ = make_product(url="htts://unexisting.url.polytech.usa")

        self.assertEqual(str(ex_info.value), str(InvalidUrlException(url="htts://unexisting.url.polytech.usa")))

    @mock.patch("webdriver_manager.chrome.ChromeDriverManager.__new__", side_effect=InvalidArgumentException)
    def test_make_product_invalid_url_exception3(self, mock_chromge_driver_manager_new):
        with pytest.raises(InvalidUrlException) as ex_info:
            _ = make_product(url="http://vk.com")

        self.assertEqual(str(ex_info.value), str(InvalidUrlException(url="http://vk.com")))

    @mock.patch("webdriver_manager.chrome.ChromeDriverManager.__new__", side_effect=WebDriverException)
    def test_make_product_unexisting_url_exception1(self, mock_chromge_driver_manager_new):
        with pytest.raises(UnexistingUrlException) as ex_info:
            _ = make_product(url="someurl")

        self.assertEqual(str(ex_info.value), str(UnexistingUrlException(url="someurl")))
    @mock.patch("webdriver_manager.chrome.ChromeDriverManager.__new__", side_effect=WebDriverException)
    def test_make_product_unexisting_url_exception2(self, mock_chromge_driver_manager_new):
        with pytest.raises(UnexistingUrlException) as ex_info:
            _ = make_product(url="http://vk.com")

        self.assertEqual(str(ex_info.value), str(UnexistingUrlException(url="http://vk.com")))

    @mock.patch("webdriver_manager.chrome.ChromeDriverManager.__new__", side_effect=WebDriverException)
    def test_make_product_unexisting_url_exception3(self, mock_chromge_driver_manager_new):
        with pytest.raises(UnexistingUrlException) as ex_info:
            _ = make_product(url="htts://unexisting.url.polytech.usa")

        self.assertEqual(str(ex_info.value), str(UnexistingUrlException(url="htts://unexisting.url.polytech.usa")))

    def test_make_product_no_parse1(self):
        product = make_product(url="http://myurl.ru", no_parse=True)

        self.assertEqual(product.url, 'http://myurl.ru')
        self.assertEqual(product.title, '</>')
        self.assertEqual(product.vendor, '</>')

    def test_make_product_no_parse2(self):
        product = make_product(url="htts://unexisting.url.polytech.usa", no_parse=True)

        self.assertEqual(product.url, 'htts://unexisting.url.polytech.usa')
        self.assertEqual(product.title, '</>')
        self.assertEqual(product.vendor, '</>')

    def test_make_product_no_parse3(self):
        product = make_product(url="not_valid_url", no_parse=True)

        self.assertEqual(product.url, 'not_valid_url')
        self.assertEqual(product.title, '</>')
        self.assertEqual(product.vendor, '</>')

    @mock.patch("selenium.webdriver.support.ui.WebDriverWait.__new__")
    @mock.patch("selenium.webdriver.Chrome.__new__")
    @mock.patch("selenium.webdriver.chrome.service.Service.__new__")
    @mock.patch("webdriver_manager.chrome.ChromeDriverManager.__new__")
    def test_get_price1(
        self,
        mock_chromge_driver_manager_new,
        mock_webdriver_service_new,
        mock_webdriver_chrome_new,
        mock_webdriver_wait_new,
    ):
        chrome_driver_manager_new_mock = mock.MagicMock(name='chrome_driver_manager')
        chrome_driver_manager_new_mock.install.return_value = None
        mock_chromge_driver_manager_new.return_value = chrome_driver_manager_new_mock

        service_mock = mock.MagicMock(name='service')
        mock_webdriver_service_new.return_value = service_mock

        webdriver_chrome_new_mock = mock.MagicMock(name='webdriver_chrome')
        webdriver_chrome_new_mock.get.return_value = None
        mock_webdriver_chrome_new.return_value = webdriver_chrome_new_mock

        webdriver_wait_until_mock = mock.MagicMock(name='webdriver_wait_until')
        webdriver_wait_until_mock.text = '999'

        webdriver_wait_new_mock = mock.MagicMock(name='webdriver_wait')
        webdriver_wait_new_mock.until.return_value = webdriver_wait_until_mock
        mock_webdriver_wait_new.return_value = webdriver_wait_new_mock

        product = model.Product(
            url="http://polytech.usa",
            title="oktitle",
            vendor="okvendor",
        )

        price = get_price(product=product, logger=LoggerMock())

        self.assertEqual(price.value, '999')

    @mock.patch("selenium.webdriver.support.ui.WebDriverWait.__new__")
    @mock.patch("selenium.webdriver.Chrome.__new__")
    @mock.patch("selenium.webdriver.chrome.service.Service.__new__")
    @mock.patch("webdriver_manager.chrome.ChromeDriverManager.__new__")
    def test_get_price2(
        self,
        mock_chromge_driver_manager_new,
        mock_webdriver_service_new,
        mock_webdriver_chrome_new,
        mock_webdriver_wait_new,
    ):
        chrome_driver_manager_new_mock = mock.MagicMock(name='chrome_driver_manager')
        chrome_driver_manager_new_mock.install.return_value = None
        mock_chromge_driver_manager_new.return_value = chrome_driver_manager_new_mock

        service_mock = mock.MagicMock(name='service')
        mock_webdriver_service_new.return_value = service_mock

        webdriver_chrome_new_mock = mock.MagicMock(name='webdriver_chrome')
        webdriver_chrome_new_mock.get.return_value = None
        mock_webdriver_chrome_new.return_value = webdriver_chrome_new_mock

        webdriver_wait_until_mock = mock.MagicMock(name='webdriver_wait_until')
        webdriver_wait_until_mock.text = 'string'

        webdriver_wait_new_mock = mock.MagicMock(name='webdriver_wait')
        webdriver_wait_new_mock.until.return_value = webdriver_wait_until_mock
        mock_webdriver_wait_new.return_value = webdriver_wait_new_mock

        product = model.Product(
            url="not_valid_url",
            title="sometitle",
            vendor="somevendor",
        )

        price = get_price(product=product, logger=LoggerMock())

        self.assertEqual(price.value, 'string')
    
    @mock.patch("selenium.webdriver.support.ui.WebDriverWait.__new__")
    @mock.patch("selenium.webdriver.Chrome.__new__")
    @mock.patch("selenium.webdriver.chrome.service.Service.__new__")
    @mock.patch("webdriver_manager.chrome.ChromeDriverManager.__new__")
    def test_get_price3(
        self,
        mock_chromge_driver_manager_new,
        mock_webdriver_service_new,
        mock_webdriver_chrome_new,
        mock_webdriver_wait_new,
    ):
        chrome_driver_manager_new_mock = mock.MagicMock(name='chrome_driver_manager')
        chrome_driver_manager_new_mock.install.return_value = None
        mock_chromge_driver_manager_new.return_value = chrome_driver_manager_new_mock

        service_mock = mock.MagicMock(name='service')
        mock_webdriver_service_new.return_value = service_mock

        webdriver_chrome_new_mock = mock.MagicMock(name='webdriver_chrome')
        webdriver_chrome_new_mock.get.return_value = None
        mock_webdriver_chrome_new.return_value = webdriver_chrome_new_mock

        webdriver_wait_until_mock = mock.MagicMock(name='webdriver_wait_until')
        webdriver_wait_until_mock.text = '999999999'

        webdriver_wait_new_mock = mock.MagicMock(name='webdriver_wait')
        webdriver_wait_new_mock.until.return_value = webdriver_wait_until_mock
        mock_webdriver_wait_new.return_value = webdriver_wait_new_mock

        product = model.Product(
            url="http://vk.com",
            title="vkmusic",
            vendor="vk",
        )

        price = get_price(product=product, logger=LoggerMock())

        self.assertEqual(price.value, '999999999')


class TestExceptions(unittest.TestCase):
    def test_already_exists_message1(self):
        exception = InvalidUrlException(url="hello")
        self.assertEqual(str(exception), "invalid URL (hello)")

    def test_already_exists_message2(self):
        exception = InvalidUrlException(url="http://vk.com")
        self.assertEqual(str(exception), "invalid URL (http://vk.com)")

    def test_already_exists_message3(self):
        exception = InvalidUrlException(url="http://polytech.learning.usa")
        self.assertEqual(str(exception), "invalid URL (http://polytech.learning.usa)")

    def test_not_found_message1(self):
        exception = UnexistingUrlException(url="goodbye")
        self.assertEqual(str(exception), "unexisting URL\n(goodbye)")
    
    def test_not_found_message2(self):
        exception = UnexistingUrlException(url="http://vk.com")
        self.assertEqual(str(exception), "unexisting URL\n(http://vk.com)")

    def test_not_found_message3(self):
        exception = UnexistingUrlException(url="http://polytech.learning.usa")
        self.assertEqual(str(exception), "unexisting URL\n(http://polytech.learning.usa)")
