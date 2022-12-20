from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

from columns import aria2
from .. import config


def keyboard(key_type="Normal"):
    markup = ReplyKeyboardMarkup(row_width=10)
    if key_type == "Normal":
        row = [KeyboardButton("aria2c")]
        markup.add(*row)
        row = [KeyboardButton("Exit")]
        markup.add(*row)
    elif key_type == "Aria2c":
        row = [
            KeyboardButton("➕添加任务"),
            KeyboardButton("▶️正在下载"),
            KeyboardButton("⏸︎暂停任务"),
            KeyboardButton("⏩️继续任务"),
        ]
        markup.add(*row)
        markup.add(
            KeyboardButton("☑️已完成"), KeyboardButton("❌删除任务"), KeyboardButton("退出")
        )
    elif key_type == "Remove":
        markup = ReplyKeyboardRemove()

    return markup


def inline_keyboard(key_type):
    markup = InlineKeyboardMarkup()
    if key_type == "暂停任务":
        d = aria2._tgbot_tmp.format_pause_download()

        markup.row_width = 1
        if isinstance(d, str):
            return
        for k, v in d.items():
            markup.add(
                InlineKeyboardButton(k, callback_data="暂停任务_" + v),
            )
    elif key_type == "继续任务":
        d = aria2._tgbot_tmp.format_download_pause()
        markup.row_width = 1
        if isinstance(d, str):
            return
        for k, v in d.items():
            markup.add(
                InlineKeyboardButton(k, callback_data="继续任务_" + v),
            )
    elif key_type == "删除任务":
        d = aria2._tgbot_tmp.format_acivate_paused_stop()
        markup.row_width = 1
        if isinstance(d, str):
            return
        markup.add(
            InlineKeyboardButton("删除正在下载", callback_data="删除正在下载"),
            InlineKeyboardButton("删除已暂停", callback_data="删除已暂停"),
            InlineKeyboardButton("删除已完成", callback_data="删除已完成"),
            InlineKeyboardButton("删除错误任务", callback_data="删除错误"),
            InlineKeyboardButton("删除removed", callback_data="删除removed"),
            InlineKeyboardButton("删除所有", callback_data="删除所有"),
        )
        for k, v in d.items():
            markup.add(
                InlineKeyboardButton(k, callback_data="删除_" + v.get("gid")),
            )
    return markup


def inline_callback(call, bot: TeleBot):
    n = 0
    if call.json["message"]["text"] == "请点击要暂停的任务":
        _aria2_tmp = aria2.Aria2_do(config.ARIA2_URL, config.ARIA2_SECREAT)
        _aria2_tmp.pause(call.data.split("_")[1])
        bot.answer_callback_query(call.id, "paused")
        while n < 5:
            try:
                time.sleep(1)
                bot.edit_message_reply_markup(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=inline_keyboard("暂停任务"),
                )
                break
            except Exception as e:
                print(e)
                n += 1
    elif call.json["message"]["text"] == "请点击要继续的任务":
        _aria2_tmp = aria2.Aria2_do(config.ARIA2_URL, config.ARIA2_SECREAT)
        _aria2_tmp.un_pause(call.data.split("_")[1])
        bot.answer_callback_query(call.id, "started")
        while n < 5:
            try:
                time.sleep(1)
                bot.edit_message_reply_markup(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=inline_keyboard("继续任务"),
                )
                break
            except Exception as e:
                print(e)
                n += 1
    elif call.json["message"]["text"] == "请点击要删除的任务":
        _aria2_tmp = aria2.Aria2_do(config.ARIA2_URL, config.ARIA2_SECREAT)
        if call.data.split("_")[0] != "删除":
            d = aria2._tgbot_tmp.format_acivate_paused_stop()
            if call.data.split("_")[0] == "删除正在下载":
                _tasks_do = [
                    v.get("gid") for v in d.values() if v.get("status") == "active"
                ]
            elif call.data.split("_")[0] == "删除已暂停":

                _tasks_do = [
                    v.get("gid") for v in d.values() if v.get("status") == "paused"
                ]
            elif call.data.split("_")[0] == "删除已完成":
                _tasks_do = [
                    v.get("gid") for v in d.values() if v.get("status") == "complete"
                ]
            elif call.data.split("_")[0] == "删除错误":
                _tasks_do = [
                    v.get("gid") for v in d.values() if v.get("status") == "error"
                ]
            elif call.data.split("_")[0] == "删除removed":
                _tasks_do = [
                    v.get("gid") for v in d.values() if v.get("status") == "removed"
                ]
            elif call.data.split("_")[0] == "删除所有":
                _tasks_do = [v.get("gid") for v in d.values()]
            for i in _tasks_do:
                if i != "":
                    _aria2_tmp.remove_noerror(i)
        else:
            _aria2_tmp.remove_noerror(call.data.split("_")[1])
        if call.data.split("_")[0] == "删除正在下载":
            bot.answer_callback_query(
                call.id,
                "please click 删除removed again.",
            )
        else:
            bot.answer_callback_query(call.id, "deleted")
        while n < 5:
            try:
                time.sleep(1)
                bot.edit_message_reply_markup(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=inline_keyboard("删除任务"),
                )
                break
            except Exception as e:
                print(e)
                n += 1
