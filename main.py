# code by @HORRIDduo

from pyrogram import Client, filters
from settings import *
from utils.message import *
from pyrogram.types import *
import logging

logging.basicConfig(level=logging.INFO)

bot = Client("bot", api_id=27215224, api_hash="688ae67db37f0ae991c3ecb97d73ff0a", bot_token="7851237202:AAEszK9R4Sr99thXEiQnFbV8K4nFu9Ksjew")

@bot.on_message(filters.command("run"))
async def run(client, message):
    lang, code = message.text.split(maxsplit=2)[1:]
    request = RunRequest(lang, code)
    response = execute_code(request)   
    await message.reply(f"Output: {response}") 

@bot.on_message(filters.command("langs"))
async def langs(client, message):
    await message.reply_text(LANGS)

@bot.on_inline_query()
async def inline(client, query):
    text = query.query
    lang, code = text.split(maxsplit=1)
    request = RunRequest(lang, code)
    if not execute_code(request):
        await query.answer([
            InlineQueryResultArticle(
                title="Bad Query",
                description="usage: @GoodCodeRunBot [language] [code]",
                input_message_content=InputTextMessageContent(HOW_INLINE)
            )
        ])
    else:
        response = execute_code(request)
        await query.answer([
            InlineQueryResultArticle(
                title="Output",
                description=f"{response}",
                input_message_content=InputTextMessageContent(INLINE.format(lang, code, response))
            )
        ])

print("bot is working 🥰")
bot.run()
