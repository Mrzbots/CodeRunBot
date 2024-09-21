from pyrogram import filters
from settings import *
from pyrogram.types import *
from main import bot

@bot.on_message(filters.command("run"))
async def run(client, message):
    lang, code = message.text.split(maxsplit=2)[1:]
    request = RunRequest(lang, code)
    response = execute_code(request)   
    await message.reply(f"Output: {response}")
