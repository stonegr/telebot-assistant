# filters
from tgbot import filters

# handlers
from tgbot import handlers

# from tgbot.handlers.

# middlewares
from tgbot.middlewares.antiflood_middleware import antispam_func

# states
from tgbot.states.register_state import Register

# utils
from tgbot.utils.database import Database

# telebot
from telebot import TeleBot

# config
from tgbot import config

# proxy
if config.HTTP_PROXY:
    from telebot import apihelper

    apihelper.proxy = {"http": config.HTTP_PROXY, "https": config.HTTP_PROXY}

db = Database()

# remove this if you won't use middlewares:
from telebot import apihelper

apihelper.ENABLE_MIDDLEWARE = True

# I recommend increasing num_threads
bot = TeleBot(config.TOKEN, num_threads=5)


def register_handlers():
    bot.register_message_handler(
        handlers.admin_user, commands=["start"], admin=True, pass_bot=True
    )
    bot.register_message_handler(
        handlers.any_user,
        commands=["start"],
        admin=False,
        allow_user=True,
        pass_bot=True,
    )
    bot.register_message_handler(
        handlers.notaccess_handle,
        commands=["start"],
        admin=False,
        allow_user=False,
        pass_bot=True,
    )
    bot.register_message_handler(
        handlers.reset_handle, commands=["reset"], allow_user=True, pass_bot=True
    )
    # 抖音
    bot.register_message_handler(
        handlers.douyin_handle, commands=["douyin"], allow_user=True, pass_bot=True
    )

    # menu
    bot.register_message_handler(
        handlers.menu_handle, commands=["menu"], allow_user=True, pass_bot=True
    )

    # callback handler
    bot.register_callback_query_handler(
        handlers.inline_callback, func=lambda call: True, pass_bot=True
    )


register_handlers()

# Middlewares
bot.register_middleware_handler(antispam_func, update_types=["message"])


# custom filters
bot.add_custom_filter(filters.AdminFilter())
bot.add_custom_filter(filters.AllowFilter())

# aria2c 下载检测
from columns import aria2

aria2.Moniter_active(bot)
aria2.Flush_data()

# bot.enable_save_next_step_handlers(delay=2)
# bot.load_next_step_handlers()

# bot.enable_save_next_step_handlers(delay=2)
# bot.load_next_step_handlers()


def run():
    bot.infinity_polling(skip_pending=True)


run()
