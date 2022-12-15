from telebot import TeleBot
from telebot.types import Message


def notaccess_handle(message: Message, bot: TeleBot):
    """
    You can create a function and use parameter pass_bot.
    """

    if bot.temp_data:
        if bot.temp_data.get(message.from_user.id) != "OK":
            return

    bot.reply_to(message, "未授权")
