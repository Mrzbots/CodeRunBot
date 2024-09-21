# code by @HORRIDduo

from settings import *
from pyrogram.types import *
from main import bot

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
