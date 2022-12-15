from telebot.types import Message
from telebot import TeleBot

import time
from ..handlers.keyboard import keyboard

DATA = {}


def antispam_func(bot: TeleBot, message: Message):
    bot.temp_data = {message.from_user.id: "OK"}
    if DATA.get(message.from_user.id):
        # print(int(time.time()) - DATA[message.from_user.id])
        if int(time.time()) - DATA[message.from_user.id] < 2:
            bot.temp_data = {message.from_user.id: "FAIL"}
            bot.send_message(
                message.chat.id,
                "You are making request too often",
                reply_markup=keyboard("Remove"),
            )
    DATA[message.from_user.id] = message.date
