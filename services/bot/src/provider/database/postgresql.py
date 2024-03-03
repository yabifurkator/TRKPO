import os
import logging

import psycopg2
from psycopg2.errors import UniqueViolation

from model import model
from .exceptions import AlreadyExistsException, NotFoundException


def make_entry(product: model.Product, user: model.User) -> model.Entry:
    return model.Entry(product=product, user=user)


def insert_entry(entry: model.Entry, logger: logging.Logger):
    try:
        logger.info("establishing connection to database")
        with psycopg2.connect(
            host="database",
            port="5432",
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            database=os.environ['POSTGRES_DB'],
        ) as connection:
            with connection.cursor() as cursor:
                sql_request = (
                    f"INSERT INTO products (url, title, vendor, user_telegram_id) "
                    f"VALUES ('{entry.product.url}', '{entry.product.title}', '{entry.product.vendor}', '{entry.user.telegramID}')"
                )

                logger.info(f"quering sql: {sql_request}")
                cursor.execute(sql_request)
    except UniqueViolation:
        raise AlreadyExistsException()
    

def list_entries(logger: logging.Logger) -> list[model.Entry]:
    with psycopg2.connect(
        host="database",
        port="5432",
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        database=os.environ['POSTGRES_DB'],
    ) as connection:
        with connection.cursor() as cursor:

            sql_request = (
                f"SELECT url, title, vendor, user_telegram_id FROM products"
            )

            logger.info(f"quering sql: {sql_request}")
            cursor.execute(sql_request)

            entry_list: list[model.Entry] = []

            rows = cursor.fetchall()
            logger.info(f"sql response: {rows}")

            for row in rows:
                entry = model.Entry(
                    product=model.Product(
                        url=row[0],
                        title=row[1],
                        vendor=row[2],
                    ),
                    user=model.User(
                        telegramID=row[3],
                    ),
                )

                entry_list.append(entry)

            return entry_list 


def delete_entry(entry: model.Entry, logger: logging.Logger):
    logger.info("establishing connection to database")
    with psycopg2.connect(
        host="database",
        port="5432",
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        database=os.environ['POSTGRES_DB'],
    ) as connection:
        with connection.cursor() as cursor:
            sql_request = (
                f"DELETE FROM products "
                f"WHERE url='{entry.product.url}' AND user_telegram_id='{entry.user.telegramID}'"
            )

            logger.info(f"quering sql: {sql_request}")
            cursor.execute(sql_request)

            if cursor.rowcount == 0:
                raise NotFoundException()
