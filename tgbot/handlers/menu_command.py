import telebot
from telebot import TeleBot
from telebot.types import Message

from .keyboard import keyboard

from .aria2c.aria2c_commond import aria2_handle


def menu_handle(message: Message, bot: TeleBot):
    """
    You can create a function and use parameter pass_bot.
    """

    if bot.temp_data:
        if bot.temp_data.get(message.from_user.id) != "OK":
            return
    msg = bot.reply_to(message, "已显示menu", reply_markup=keyboard("Normal"))
    bot.register_next_step_handler(msg, menu_parse, bot)


def menu_parse(message: Message, bot: TeleBot):
    """
    解析menu
    """

    msg = ""

    if message.text == "Exit":
        msg = bot.reply_to(message, "已退出", reply_markup=keyboard("Remove"))
    elif message.text == "aria2c":
        msg = bot.reply_to(message, "aria2菜单", reply_markup=keyboard("Aria2c"))
        bot.register_next_step_handler_by_chat_id(message.chat.id, aria2_handle, bot)
    else:
        if not msg:
            msg = bot.reply_to(message, "输入错误,请重新输入!")
        bot.register_next_step_handler(msg, menu_parse, bot)
