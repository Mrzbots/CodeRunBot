# (c) @HORRIDduo

from pyrogram import Client, filters
from settings import *
from utils.message import *
from pyrogram.types import *


@Client.on_message(filters.command("langs"))
async def langs(client, message):
    await message.reply_text(LANGS)

@Client.on_message(filters.command("help"))
async def help(client, message):
    await message.reply_text(HELP)

@Client.on_message(filters.command("start"))
async def start(client, message):
    buttons = [
        [InlineKeyboardButton("Support Group", url="https://t.me/XBOTSUPPORTS")],
        [InlineKeyboardButton("Source Code", url="https://github.com/Mrzbots/CodeRunBot")]
    ]
    await message.reply_text(START, reply_markup=InlineKeyboardMarkup(buttons))
    
