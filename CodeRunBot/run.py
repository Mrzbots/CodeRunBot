from pyrogram import Client, filters
from settings import *
from utils.message import *
from pyrogram.types import *
from .button import get_reply_markup

@Client.on_message(filters.command("run"))
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
      
