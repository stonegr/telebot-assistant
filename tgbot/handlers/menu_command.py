import telebot
from telebot import TeleBot
from telebot.types import Message
import re

from .keyboard import keyboard, inline_keyboard


import basic
from columns import aria2, douyin
from .. import config


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
    elif message.text == "douyin":
        msg = bot.reply_to(message, "请输入链接")
        bot.register_next_step_handler_by_chat_id(message.chat.id, douyin_parse, bot)
    else:
        if not msg:
            msg = bot.reply_to(message, "输入错误,请重新输入!")
        bot.register_next_step_handler(msg, menu_parse, bot)


# aria2c
def aria2_handle(message: Message, bot: TeleBot):
    """
    You can create a function and use parameter pass_bot.
    """

    if bot.temp_data:
        if bot.temp_data.get(message.from_user.id) != "OK":
            return

    msg = ""
    if message.text == "退出":
        msg = bot.reply_to(message, "已退出", reply_markup=keyboard("Normal"))
        bot.register_next_step_handler(msg, menu_parse, bot)
        return
    elif message.text == "➕添加任务":
        msg = bot.reply_to(
            message,
            "请输入下载链接, 多个以;分割",
        )
        bot.register_next_step_handler(msg, add_aria2_task, bot)
        return
    elif message.text == "▶️正在下载":
        _aria2_downloading = aria2._tgbot_tmp.format_downloading()
        msg = bot.reply_to(
            message,
            _aria2_downloading,
        )
    elif message.text == "☑️已完成":
        _aria2_paused = aria2._tgbot_tmp.format_stoped()
        msg = bot.reply_to(
            message,
            _aria2_paused,
        )
    elif message.text == "❌删除任务":
        _inline_btn = inline_keyboard("删除任务")
        if _inline_btn:
            msg = bot.reply_to(message, "请点击要删除的任务", reply_markup=_inline_btn)
        else:
            msg = bot.reply_to(message, "无可删除任务")
    elif message.text == "⏸︎暂停任务":
        _inline_btn = inline_keyboard("暂停任务")
        if _inline_btn:
            msg = bot.reply_to(message, "请点击要暂停的任务", reply_markup=_inline_btn)
        else:
            msg = bot.reply_to(message, "无可暂停任务")

    elif message.text == "⏩️继续任务":
        _inline_btn = inline_keyboard("继续任务")
        if _inline_btn:
            msg = bot.reply_to(message, "请点击要继续的任务", reply_markup=_inline_btn)
        else:
            msg = bot.reply_to(message, "无可继续任务")

    if not msg:
        msg = bot.reply_to(message, "输入错误,请重新输入!")
    bot.register_next_step_handler(msg, aria2_handle, bot)


def add_aria2_task(message: Message, bot: TeleBot):
    _aria2_tmp = aria2.Aria2_do(config.ARIA2_URL, config.ARIA2_SECREAT)
    try:
        for i in message.text.split(";"):
            _aria2_tmp.add_uri(i)
        bot.reply_to(message, "已添加")
    except:
        bot.reply_to(message, "格式错误,请重试")
    bot.register_next_step_handler_by_chat_id(message.chat.id, aria2_handle, bot)


# douyin
def douyin_parse(message: Message, bot: TeleBot):
    """
    解析抖音链接
    """

    if not re.findall(r"http[s]?://v.douyin.com/\S+", message.text):
        bot.reply_to(message, "未检测到url, 已退出!")
    else:
        judged_url = douyin.get_douyin(message.text)
        bot.reply_to(message, basic.Format_json(judged_url)),
    bot.register_next_step_handler_by_chat_id(message.chat.id, menu_parse, bot)
