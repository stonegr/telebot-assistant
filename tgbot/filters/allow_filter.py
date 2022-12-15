from telebot.custom_filters import SimpleCustomFilter
from tgbot.models.users_model import Allow


class AllowFilter(SimpleCustomFilter):
    """
    Filter for allow allow_user
    """

    key = "allow_user"

    def check(self, message):

        return int(message.chat.id) in Allow.Allow.value
