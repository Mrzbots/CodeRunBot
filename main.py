from pyrogram import Client, filters
from settings import *
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

bot = Client("my_bot", api_id=27215224, api_hash="688ae67db37f0ae991c3ecb97d73ff0a", bot_token="7851237202:AAEszK9R4Sr99thXEiQnFbV8K4nFu9Ksjew")

@bot.on_message(filters.command("run"))
async def run_code_command(client, message):
    lang, code = message.text.split(maxsplit=2)[1:]
    request = RunRequest(lang, code)
    response = execute_code(request)   
    await message.reply(f"Output: {response}")

@bot.on_inline_query()
async def inline_run_code(client, inline_query):    
    text = inline_query.query
    print(text)
    lang = text.split(maxsplit=1)[0]
    print(lang)
    code = text.split(maxsplit=1)[1]
    print(code)
    request = RunRequest(lang, code)
    response = execute_code(request)
    await inline_query.answer([
        InlineQueryResultArticle(
            title="Run Code",
            description=f"Output: {response}",
            input_message_content=InputTextMessageContent(f"Output: {response}")
        )
    ])
    
        
bot.run()
