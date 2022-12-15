import telebot
from telebot import TeleBot
from telebot.types import Message

import re

import columns, basic


def douyin_handle(message: Message, bot: TeleBot):
    """
    You can create a function and use parameter pass_bot.
    """

    if bot.temp_data:
        if bot.temp_data.get(message.from_user.id) != "OK":
            return
    msg = bot.reply_to(message, "请输入链接")
    bot.register_next_step_handler(msg, douyin_parse, bot)


def douyin_parse(message: Message, bot: TeleBot):
    """
    解析抖音链接
    """

    if not re.findall(r"http[s]?://v.douyin.com/\S+", message.text):
        return bot.reply_to(message, "未检测到url, 已退出!")

    judged_url = columns.get_douyin(message.text)
    bot.reply_to(message, basic.Format_json(judged_url)),
