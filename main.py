from pyrogram import Client, filters
from settings import *
from utils.message import *
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

bot = Client("my_bot", api_id=27215224, api_hash="688ae67db37f0ae991c3ecb97d73ff0a", bot_token="7851237202:AAEszK9R4Sr99thXEiQnFbV8K4nFu9Ksjew")

@bot.on_message(filters.command("run"))
async def ru(client, message):
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
    lang = text.split(maxsplit=1)[0]
    code = text.split(maxsplit=1)[1]
    request = RunRequest(lang, code)
    response = execute_code(request)
    await query.answer([
        InlineQueryResultArticle(
            title="Run Code",
            description=f"Output: {response}",
            input_message_content=InputTextMessageContent(f"Output: {response}")
        )
    ])
    
        
bot.run()
