import logging

from telebot import TeleBot
from telebot import types

from model import model

from provider.web import wildberries
from provider.platform import telegram
from provider.database import postgresql
from provider.database.exceptions import NotFoundException


def delete_controller(bot: TeleBot, message: types.Message, logger: logging.Logger):
    logger.info(f"sending a relpy message to user message")
    reply_message = bot.reply_to(
        message=message,
        text="please, send me a link to the product ↓",
    )

    logger.info(f"registration callback on user reply")
    bot.register_next_step_handler(
        message=reply_message,
        callback=delete_controller_callback,
        bot=bot,
        logger=logger,
    )

    
def delete_controller_callback(user_reply: types.Message, bot: TeleBot, logger: logging.Logger): 
    logger.info(f"user_reply: {user_reply}")
    try:
        product = wildberries.make_product(url=user_reply.text, no_parse=True)
        user = telegram.make_user(user_id=user_reply.from_user.id)
        entry = postgresql.make_entry(product=product, user=user)

        postgresql.delete_entry(entry=entry, logger=logger)
        bot.reply_to(message=user_reply, text="successfully deleted product from database")

    except NotFoundException as ex:
        reply = f"failed to delete product: {ex}" 
        logger.error(reply)
        bot.reply_to(message=user_reply, text=reply)


