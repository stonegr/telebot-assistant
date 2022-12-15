from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

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
        _aria2_tmp = aria2.Aria2_do(config.ARIA2_URL, config.ARIA2_SECREAT)
        d = _aria2_tmp.format_pause_download()

        markup.row_width = 1
        if isinstance(d, str):
            return
        for k, v in d.items():
            markup.add(
                InlineKeyboardButton(k, callback_data="暂停任务_" + v),
            )
    elif key_type == "继续任务":
        _aria2_tmp = aria2.Aria2_do(config.ARIA2_URL, config.ARIA2_SECREAT)
        d = _aria2_tmp.format_download_pause()
        markup.row_width = 1
        if isinstance(d, str):
            return
        for k, v in d.items():
            markup.add(
                InlineKeyboardButton(k, callback_data="继续任务_" + v),
            )
    elif key_type == "删除任务":
        _aria2_tmp = aria2.Aria2_do(config.ARIA2_URL, config.ARIA2_SECREAT)
        d = _aria2_tmp.format_acivate_paused_stop()
        markup.row_width = 1
        if isinstance(d, str):
            return
        _tasks_active = [
            v.get("gid") for v in d.values() if v.get("status") == "active"
        ]
        _tasks_pause = [v.get("gid") for v in d.values() if v.get("status") == "paused"]
        _tasks_stop = [
            v.get("gid") for v in d.values() if v.get("status") == "complete"
        ]
        _tasks_error = [v.get("gid") for v in d.values() if v.get("status") == "error"]
        _tasks_removed = [
            v.get("gid") for v in d.values() if v.get("status") == "removed"
        ]
        _tasks_all = [v.get("gid") for v in d.values()]
        markup.add(
            InlineKeyboardButton(
                "删除正在下载", callback_data="删除正在下载_" + ";".join(_tasks_active)
            ),
            InlineKeyboardButton(
                "删除已暂停", callback_data="删除已暂停_" + ";".join(_tasks_pause)
            ),
            InlineKeyboardButton(
                "删除已完成", callback_data="删除已完成_" + ";".join(_tasks_stop)
            ),
            InlineKeyboardButton(
                "删除错误任务", callback_data="删除错误_" + ";".join(_tasks_error)
            ),
            InlineKeyboardButton(
                "删除removed", callback_data="删除removed_" + ";".join(_tasks_removed)
            ),
            # InlineKeyboardButton("删除所有", callback_data="删除所有_" + ";".join(_tasks_all)),
        )
        for k, v in d.items():
            markup.add(
                InlineKeyboardButton(k, callback_data="删除_" + v.get("gid")),
            )
    return markup


def inline_callback(call, bot: TeleBot):
    if call.json["message"]["text"] == "请点击要暂停的任务":
        _aria2_tmp = aria2.Aria2_do(config.ARIA2_URL, config.ARIA2_SECREAT)
        _aria2_tmp.pause(call.data.split("_")[1])
        bot.answer_callback_query(call.id, "paused")
    elif call.json["message"]["text"] == "请点击要继续的任务":
        _aria2_tmp = aria2.Aria2_do(config.ARIA2_URL, config.ARIA2_SECREAT)
        _aria2_tmp.un_pause(call.data.split("_")[1])
        bot.answer_callback_query(call.id, "started")
    elif call.json["message"]["text"] == "请点击要删除的任务":
        _aria2_tmp = aria2.Aria2_do(config.ARIA2_URL, config.ARIA2_SECREAT)
        if call.data.split("_")[0] != "删除":
            for i in call.data.split("_")[1].split(";"):
                if i != "":
                    _aria2_tmp.remove_noerror(i)
        else:
            _aria2_tmp.remove_noerror(call.data.split("_")[1])
        bot.answer_callback_query(call.id, "deleted")
