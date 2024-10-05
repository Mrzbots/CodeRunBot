# (c) @HORRIDduo

from pyrogram import Client
from settings import *
from .button import *
from utils.message import *
from pyrogram.types import *

@Client.on_inline_query()
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
        

         
