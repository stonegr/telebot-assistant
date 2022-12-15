import telebot
from telebot import TeleBot
from telebot.types import Message

from ..commond import base_commond


def admin_user(message: Message, bot: TeleBot):
    """
    You can create a function and use parameter pass_bot.
    """
    if bot.temp_data:
        if bot.temp_data.get(message.from_user.id) != "OK":
            return

    bot.send_message(message.chat.id, "Hello, admin!")
    bot.set_my_commands(**base_commond(message.chat.id))
