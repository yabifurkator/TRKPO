import logging

from telebot import types
from telebot import TeleBot

from model import model
from view import view

from provider.web import wildberries
from provider.database import postgresql
from provider.platform import telegram
from provider.web.exceptions import InvalidUrlException, UnexistingUrlException
from provider.database.exceptions import AlreadyExistsException


def add_controller(bot: TeleBot, message: types.Message, logger: logging.Logger):
    logger.info(f"sending a relpy message to user message")
    reply_message = bot.reply_to(
        message=message,
        text="please, send me a link to the product ↓",
    )

    logger.info(f"registration callback on user reply")
    bot.register_next_step_handler(
        message=reply_message,
        callback=add_controller_callback,
        bot=bot,
        logger=logger,
    )


def add_controller_callback(user_reply: types.Message, bot: TeleBot, logger: logging.Logger):
    logger.info(f"user_reply: {user_reply}")

    try:
        product: model.Product = wildberries.make_product(url=user_reply.text)
        user: model.User = telegram.make_user(user_id=user_reply.from_user.id)
        entry: model.Entry = postgresql.make_entry(product=product, user=user)

        postgresql.insert_entry(entry=entry, logger=logger)
        
        logger.info(f"sucessfully added new product to database\n{view.Product(product=product)}\n{view.User(user=user)}")
        bot.send_message(user_reply.chat.id, "successfully added new product to database")

    except (InvalidUrlException, UnexistingUrlException, AlreadyExistsException) as ex:
        message = f"failed to add new product: {ex}" 
        logger.error(message)
        bot.reply_to(message=user_reply, text=message)

    except Exception as ex:
        logger.exception(f"failed to add new product\nunknown exception: {ex}\nwith type: {type(ex)}")
        bot.reply_to(message=user_reply, text=f"failed to add new product: unknown exception")
