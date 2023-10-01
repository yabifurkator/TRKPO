import logging

from telebot import TeleBot
from telebot import types

from view import view
from model import model
from provider.database import postgresql
from provider.platform import telegram
from provider.web import wildberries


def getprices_controller(bot: TeleBot, message: types.Message, logger: logging.Logger):
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

    for entry in user_entries:
        product_with_price = view.ProductWithPrice(
            product=entry.product,
            price=wildberries.get_price(product=entry.product, logger=logger),
        )

        reply += f"\n{product_with_price}\n"
        reply += view.LINES

    logger.info(f"prices:::\n{reply}")

    bot.reply_to(message=message, text=f"prices:\n{reply}")
