import telebot


def base_commond(chat_id: int):
    return {
        "commands": [
            telebot.types.BotCommand("reset", "恢复默认命令"),
            telebot.types.BotCommand("menu", "任务菜单"),
            telebot.types.BotCommand("douyin", "抖音无水印解析"),
        ],
        "scope": telebot.types.BotCommandScopeChat(chat_id),
    }
