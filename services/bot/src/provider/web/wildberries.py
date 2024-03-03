import time
import requests
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException, WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from model import model
from .exceptions import InvalidUrlException, UnexistingUrlException


DEFAULT_WEBDRIVER_PARCE_DELAY = 3.0 # seconds


def make_product(url: str, no_parse=False) -> model.Product:
    if no_parse:
        return model.Product(url=url, title="</>", vendor="</>")

    try:
        service = Service(ChromeDriverManager().install()) 
        options = Options()
        options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--start-maximized')

        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url=url)

        product_header: WebElement = WebDriverWait(
            driver=driver,
            timeout=DEFAULT_WEBDRIVER_PARCE_DELAY,
        ).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-page__header')))

        vendor = product_header.find_element(By.TAG_NAME, 'a').text
        title = product_header.find_element(By.TAG_NAME, 'h1').text

        return model.Product(url=url, title=title, vendor=vendor)

    except InvalidArgumentException:
        raise InvalidUrlException(url=url)

    except WebDriverException:
        raise UnexistingUrlException(url=url)
    

def get_price(product: model.Product, logger: logging.Logger) -> model.Price:
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url=product.url)

    price_element: WebElement = WebDriverWait(
        driver=driver,
        timeout=DEFAULT_WEBDRIVER_PARCE_DELAY,
    ).until(EC.presence_of_element_located((By.CLASS_NAME, 'price-block__final-price')))

    value = price_element.text

    return model.Price(value=value)
