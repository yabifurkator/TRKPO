import logging

from telebot import TeleBot
from telebot import types

from provider.database import postgresql
from provider.platform import telegram

from model import model
from view import view


def list_controller(bot: TeleBot, message: types.Message, logger: logging.Logger):
    all_entries: list[model.Entry] = postgresql.list_entries(logger=logger)

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
            reply += f"\n{view.Product(product=entry.product)}\n"
            reply += view.LINES
    else:
        reply += "\nnot found"

    bot.reply_to(message=message, text=f"products:\n{reply}")
