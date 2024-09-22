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
    
    if len(parts) != 2:
        await query.answer([
            InlineQueryResultArticle(
                title="Bad Query",
                description="Usage: @GoodCodeRunBot [language] [code]",
                input_message_content=InputTextMessageContent(HOW_INLINE)
            )
        ])
        return
    
    lang, code = parts
    
    if not lang:
        await query.answer([
            InlineQueryResultArticle(
                title="Bad Query",
                description="Usage: @GoodCodeRunBot [language] [code]",
                input_message_content=InputTextMessageContent(HOW_INLINE)
            )
        ])
        return
    
    if not code:
        await query.answer([
            InlineQueryResultArticle(
                title="Bad Query",
                description="Usage: @GoodCodeRunBot [language] [code]",
                input_message_content=InputTextMessageContent(HOW_INLINE)
            )
        ])
        return
    
    request = RunRequest(lang, code)
    response = execute_code(request)    
    
    if 'run' in response and 'output' in response['run']:
        data = response["run"]["output"] 
        if data.strip() != '':  
            res = data
        else:
            res = result_success
        await query.answer([
            InlineQueryResultArticle(
                title="Output",
                description=f"{res}",
                input_message_content=InputTextMessageContent(INLINE.format(response["language"], code, res))
            )
        ])
    else:
        await query.answer([
            InlineQueryResultArticle(
                title="Unknown Language",
                description="Unknown language",
                input_message_content=InputTextMessageContent("<b>Hey, your language is unknown. Maybe it's a spelling mistake? If you want to see the supported languages, use the <code>/langs</code>command</b>")
            )
        ])
        
print("bot is working 🥰")
bot.run()
