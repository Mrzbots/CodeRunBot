# code by @HORRIDduo

from pyrogram import Client, filters
from settings import *
from utils.message import *
from pyrogram.types import *
import logging
from config import *

logging.basicConfig(level=logging.INFO)

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def get_reply_markup(query):
    buttons = [
        [
            InlineKeyboardButton('Run Code', switch_inline_query_current_chat=query)
        ]
    ]
    return InlineKeyboardMarkup(buttons)

@bot.on_message(filters.command("run"))
async def run(client, message):
    if len(message.command) < 2:
        return await message.reply_text(f"**Hey {message.from_user.mention},\n\nUsage: /run [language] [code]. If you want to see the list of supported languages, use /langs**")

    text_parts = message.text.split(maxsplit=2)[1:]
    query = ' '.join(text_parts)  
    if len(text_parts) != 2:
        return await message.reply_text(f"**Hey {message.from_user.mention},\n\nUsage: /run [language] [code]. If you want to see the list of supported languages, use /langs**")

    lang, code = text_parts
    request = RunRequest(lang, code)
    response = execute_code(request)
    reply_markup = get_reply_markup(query)
    if 'run' in response and 'output' in response['run']:
        data = response["run"]["output"]
        if data.strip() != '':
            res = data
        else:
            res = result_success
        await message.reply(OUTPUT.format(response["language"], response["version"], code, res), reply_markup=reply_markup)
    else:
        await message.reply(f"**Hey {message.from_user.mention}, your language is unknown. Maybe it's a spelling mistake? If you want to see the supported languages, use the /langs command**")

@bot.on_message(filters.command("langs"))
async def langs(client, message):
    await message.reply_text(LANGS)

@bot.on_message(filters.command("help"))
async def help(client, message):
    await message.reply_text(HELP)

@bot.on_message(filters.command("start"))
async def start(client, message):
    buttons = [
        [
            InlineKeyboardButton("Support Group", url="https://t.me/XBOTSUPPORTS")
        ]
    ]
    await message.reply_text(START, reply_markup=InlineKeyboardMarkup(buttons))
    
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
    reply_markup = get_reply_markup(text)
    
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
                reply_markup=reply_markup,
                input_message_content=InputTextMessageContent(OUTPUT.format(response["language"], response["version"], code, res))
            )
        ])
    else:
        await query.answer([
            InlineQueryResultArticle(
                title="Unknown Language",
                description="Unknown language",              
                input_message_content=InputTextMessageContent("Hey, your language is unknown. Maybe it's a spelling mistake? If you want to see the supported languages, use the. /langs command")
            )
        ])
        
print("bot is working 🥰")
bot.run()
