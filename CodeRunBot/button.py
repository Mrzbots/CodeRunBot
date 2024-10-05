from pyrogram.types import *


def get_reply_markup(query):
    buttons = [
        [
            InlineKeyboardButton('Run Code', switch_inline_query_current_chat=query)
        ]
    ]
    return InlineKeyboardMarkup(buttons)
  
