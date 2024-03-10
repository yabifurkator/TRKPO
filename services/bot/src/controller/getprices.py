import logging

import psycopg2
from telebot import TeleBot
from telebot import types

from view import view
from model import model
from provider.database import postgresql
from provider.platform import telegram
from provider.web.exceptions import InvalidUrlException


def getprices_controller(
    bot: TeleBot,
    message: types.Message,
    logger: logging.Logger,
    wildberries_get_price,
):
    try:
        all_entries = postgresql.list_entries(logger=logger)

        log: str = ""
        for entry in all_entries:
            log += f"\n{view.Entry(entry=entry)}"
        logger.info(f"all entries in database:{log}")

        user_entries: list[model.Entry] = telegram.list_entries(entry_list=all_entries, user_id=message.from_user.id)
        log: str = ""
        for entry in user_entries:
            log += f"\n{view.Entry(entry=entry)}"
        logger.info(f"user entries in database:{log}")

        reply = view.LINES

        if len(user_entries) > 0:
            for entry in user_entries:
                product_with_price = view.ProductWithPrice(
                    product=entry.product,
                    price=wildberries_get_price(product=entry.product, logger=logger),
                )

                reply += f"\n{product_with_price}\n"
                reply += view.LINES
        else:
            reply += "\nnot found"

        logger.info(f"prices:::\n{reply}")

        bot.send_message(chat_id=message.chat.id, text=f"prices:\n{reply}")

    except psycopg2.OperationalError as ex:
        logger.exception(f"failed to get prices: database error: {ex}")
        bot.reply_to(message=message, text=f"failed to get prices: database error")
    
    except InvalidUrlException as ex:
        message = f"failed to get prices: {ex}" 
        logger.error(message)
        bot.reply_to(message=message, text=message)
    
    except Exception as ex:
        logger.exception(f"failed to get prices\nunknown exception: {ex}\nwith type: {type(ex)}")
        bot.reply_to(message=message, text=f"failed to get prices: unknown exception: {ex}")
