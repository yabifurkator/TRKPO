import os
import logging

from telebot import types
from telebot import TeleBot

from tools.decorators import endpoint
from tools.logger import init_logger
from controller.add import add_controller
from controller.list import list_controller
from controller.delete import delete_controller
from controller.getprices import getprices_controller


BANNER = """
    ██████╗  █████╗ ██████╗  ██████╗███████╗██████╗     ██████╗  ██████╗ ████████╗
    ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗    ██╔══██╗██╔═══██╗╚══██╔══╝
    ██████╔╝███████║██████╔╝██║     █████╗  ██████╔╝    ██████╔╝██║   ██║   ██║   
    ██╔═══╝ ██╔══██║██╔══██╗██║     ██╔══╝  ██╔══██╗    ██╔══██╗██║   ██║   ██║   
    ██║     ██║  ██║██║  ██║╚██████╗███████╗██║  ██║    ██████╔╝╚██████╔╝   ██║   
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝    ╚═╝   
"""


INFO = """
PARCER BOT

/help         > show all possible commands
/add          > add new product on tracking
/list            > list all added products
/delete      > delete added product by url
/getprices > get prices of added products
"""


bot = TeleBot(token=os.environ["BOT_TOKEN"])
logger = init_logger(name="BOT", loglevel=logging.DEBUG, log_dir="/app/logs")


@endpoint(bot=bot, command='start', logger=logger)
def start_endpoint(message: types.Message):
    bot.reply_to(message=message, text=INFO)


@endpoint(bot=bot, command='help', logger=logger)
def help_endpoint(message: types.Message):
    bot.reply_to(message=message, text=INFO)


@endpoint(bot=bot, command='add', logger=logger)
def add_endpoint(message: types.Message):
    add_controller(bot=bot, message=message, logger=logger)


@endpoint(bot=bot, command='list', logger=logger)
def list_endpoint(message: types.Message):
    list_controller(bot=bot, message=message, logger=logger)


@endpoint(bot=bot, command='delete', logger=logger)
def delete_endpoint(message: types.Message):
    delete_controller(bot=bot, message=message, logger=logger)


@endpoint(bot=bot, command='getprices', logger=logger)
def getprices_endpoint(message: types.Message):
    getprices_controller(bot=bot, message=message, logger=logger)


@bot.message_handler(content_types='text')
def unknown_endnpoint(message: types.Message):
    bot.reply_to(message=message, text=f"unknown input: {message.text}\nwrite /help for see available commands")


def main():
    logger.info(BANNER)

    bot.infinity_polling()


if __name__ == '__main__':
    main()
