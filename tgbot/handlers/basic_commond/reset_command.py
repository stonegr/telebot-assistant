import telebot
from telebot import TeleBot
from telebot.types import Message


def reset_handle(message: Message, bot: TeleBot):
    """
    You can create a function and use parameter pass_bot.
    """

    if bot.temp_data:
        if bot.temp_data.get(message.from_user.id) != "OK":
            return

    bot.delete_my_commands(
        scope=telebot.types.BotCommandScopeChat(message.chat.id),
        language_code=None,
    )
    bot.reply_to(message, "已重置")
