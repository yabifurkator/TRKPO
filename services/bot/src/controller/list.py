import logging

import psycopg2
from telebot import TeleBot
from telebot import types

from provider.database import postgresql
from provider.platform import telegram

from model import model
from view import view


def list_controller(bot: TeleBot, message: types.Message, logger: logging.Logger):
    try:
        all_entries: list[model.Entry] = postgresql.list_entries(logger=logger)

        log: str = ""
        for entry in all_entries:
            log += f"\n{view.Entry(entry=entry)}"
        logger.info(f"all entries in database:{log}")

        user_entries: list[model.Entry] = telegram.list_entries(entry_list=all_entries, user_id=message.from_user.id)
        log: str = ""
        for entry in user_entries:
            log += f"\n{view.Entry(entry=entry)}"
        logger.info(f"user (id={message.from_user.id}) entries in database:{log}")


        reply = view.LINES

        if len(user_entries) > 0:
            for entry in user_entries:
                reply += f"\n{view.Product(product=entry.product)}\n"
                reply += view.LINES
        else:
            reply += "\nnot found"

        bot.send_message(chat_id=message.chat.id, text=f"products:\n{reply}")

    except psycopg2.OperationalError as ex:
        logger.exception(f"failed to list products: database error: {ex}")
        bot.reply_to(message=message, text=f"failed to list products: database error")

    except Exception as ex:
        logger.exception(f"failed to list products\nunknown exception: {ex}\nwith type: {type(ex)}")
        bot.reply_to(message=message, text=f"failed to list products: unknown exception: {ex}")
