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
    parts = text.split(maxsplit=1)
    
    # Check if the input is in the correct format
    if len(parts) != 2:
        await query.answer([
            InlineQueryResultArticle(
                title="Bad Query",
                description="usage: @GoodCodeRunBot [language] [code]",
                input_message_content=InputTextMessageContent(HOW_INLINE)
            )
        ])
        return
    
    lang, code = parts
    
    # Check if language or code is empty
    if not lang:
        await query.answer([
            InlineQueryResultArticle(
                title="Bad Query",
                description="Please specify the programming language",
                input_message_content=InputTextMessageContent(HOW_INLINE)
            )
        ])
        return
    
    if not code:
        await query.answer([
            InlineQueryResultArticle(
                title="Bad Query",
                description="Please provide the code to execute",
                input_message_content=InputTextMessageContent(HOW_INLINE)
            )
        ])
        return
    
    request = RunRequest(lang, code)
    response = execute_code(request)
    
    if response:
        await query.answer([
            InlineQueryResultArticle(
                title="Output",
                description=f"{response}",
                input_message_content=InputTextMessageContent(INLINE.format(lang, code, response))
            )
        ])
    else:
        await query.answer([
            InlineQueryResultArticle(
                title="Failed to Execute Code",
                description="Please check your code and try again",
                input_message_content=InputTextMessageContent(HOW_INLINE)
            )
        ])
        
print("bot is working 🥰")
bot.run()
