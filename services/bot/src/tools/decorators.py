import logging

from telebot import TeleBot
from telebot import types


def endpoint(bot: TeleBot, command: str, logger: logging.Logger):
    def decorator(func):
        @bot.message_handler(commands=[command])
        def endpoint_wrapper(message: types.Message):
            try:
                logger.warning(f"/{command} called")

                return func(message)

            except Exception as ex:
                logger.exception(f"failed to process /{command} endpoint: unexpected exception: {ex}, with type: {type(ex)}")
                bot.reply_to(message=message, text=f"failed to process /{command}: unknown exception")

        return endpoint_wrapper
    
    return decorator
