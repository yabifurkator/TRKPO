import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse

from tools.logger import init_logger
from http_server_utils.mocks import \
    UserReplyMock, \
    MessageMock, \
    BotMock, \
    wildberries_make_product_mock, \
    wildberries_get_price_mock
from http_server_utils.models import UserProduct, User
from controller.add import add_controller_callback
from controller.getprices import getprices_controller
from controller.delete import delete_controller_callback
from controller.list import list_controller


logger = init_logger(name="HTTP_SERVER", loglevel=logging.DEBUG, log_dir="/app/logs")

app = FastAPI()


@app.get("/ping")
def ping():
    return {"status": "live"}


@app.exception_handler(404)
def custom_404_handler(_, __):
    return JSONResponse(
        content={
            "command": "not found",
        },
        status_code=404,
    )


@app.post("/add")
def add(user_product: UserProduct):
    user_reply_mock = UserReplyMock(
        url=user_product.product_url,
        user_id=user_product.user_id,
    )
    bot_mock = BotMock()

    add_controller_callback(
        user_reply=user_reply_mock,
        bot=bot_mock,
        logger=logger,
        wildberries_make_product=wildberries_make_product_mock,
    )

    status_code = 200
    if bot_mock.reply_to_text == "failed to add new product: database error":
        status_code = 500
    elif bot_mock.reply_to_text == "failed to add new product: unknown exception":
        status_code = 500
    elif bot_mock.reply_to_text != "":
        status_code = 400

    return JSONResponse(
        content={
            "url": user_product.product_url,
            "user_id": user_product.user_id,
            "bot_send_message_text": bot_mock.send_message_text,
            "bot_reply_to_text": bot_mock.reply_to_text,
        },
        status_code=status_code,
    )


@app.post("/getprices")
def getprices(user: User):
    message_mock = MessageMock(
        user_id=user.user_id,
    )
    bot_mock = BotMock()

    getprices_controller(
        bot=bot_mock,
        message=message_mock,
        logger=logger,
        wildberries_get_price=wildberries_get_price_mock,
    )

    status_code = 200
    if bot_mock.reply_to_text == "failed to get prices: database error":
        status_code = 500
    elif "failed to get prices: unknown exception" in bot_mock.reply_to_text:
        status_code = 500
    elif bot_mock.reply_to_text != "":
        status_code = 400
    elif "not found" in bot_mock.send_message_text:
        status_code = 404

    return JSONResponse(
        content={
            "user_id": user.user_id,
            "bot_send_message_text": bot_mock.send_message_text,
            "bot_reply_to_text": bot_mock.reply_to_text,
        },
        status_code=status_code,
    )

@app.post("/delete")
def delete(user_product: UserProduct):
    user_reply_mock = UserReplyMock(
        url=user_product.product_url,
        user_id=user_product.user_id,
    )
    bot_mock = BotMock()

    delete_controller_callback(
        user_reply=user_reply_mock,
        bot=bot_mock,
        logger=logger,
    )

    status_code = 200
    if bot_mock.reply_to_text == "failed to delete product: not found":
        status_code = 404
    elif bot_mock.reply_to_text == "failed to delete product: database error":
        status_code = 500
    elif bot_mock.reply_to_text == "failed to delete product: unknown exception":
        status_code = 500
    elif bot_mock.reply_to_text != "":
        status_code = 400

    return JSONResponse(
        content={
            "url": user_product.product_url,
            "user_id": user_product.user_id,
            "bot_send_message_text": bot_mock.send_message_text,
            "bot_reply_to_text": bot_mock.reply_to_text,
        },
        status_code=status_code,
    )


@app.post("/list")
def list(user: User):
    message_mock = MessageMock(
        user_id=user.user_id,
    )
    bot_mock = BotMock()

    list_controller(bot=bot_mock, message=message_mock, logger=logger)

    status_code = 200
    if bot_mock.reply_to_text == "failed to list products: database error":
        status_code = 500
    elif "failed to list products: unknown exception" in bot_mock.reply_to_text:
        status_code = 500
    elif bot_mock.reply_to_text != "":
        status_code = 400
    elif "not found" in bot_mock.send_message_text:
        status_code = 404

    return JSONResponse(
        content={
            "user_id": user.user_id,
            "bot_send_message_text": bot_mock.send_message_text,
            "bot_reply_to_text": bot_mock.reply_to_text,
        },
        status_code=status_code,
    )
