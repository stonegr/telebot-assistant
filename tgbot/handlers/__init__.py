# Create files for handlers in this folder.

from tgbot.handlers.basic_commond.admin import admin_user
from tgbot.handlers.basic_commond.user import any_user
from .basic_commond.reset_command import reset_handle
from .basic_commond.not_access_command import notaccess_handle
from .menu_command import menu_handle
from .keyboard import inline_callback
