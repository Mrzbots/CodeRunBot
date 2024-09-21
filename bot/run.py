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

  
