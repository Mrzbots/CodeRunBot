from pyrogram import Client, filters
from settings import *

bot = Client("my_bot", api_id=123456, api_hash="your_api_hash", bot_token="your_bot_token")

@bot.on_message(filters.command("run"))
async def run_code(client, message):
    lang, code = message.text.split(maxsplit=2)[1:]
    request = RunRequest(lang, code, "")
    response = run_code(request)
    if response.result == RESULT_SUCCESS:
        await message.reply(f"Output: {response.output}")
    elif response.result == RESULT_ERROR:
        await message.reply(f"Error: {response.output}")
    else:
        await message.reply("Unknown error occurred")

@bot.on_inline_query(filters.regex(r"^(\w+)\s(.*)$"))
async def inline_run_code(client, inline_query):
    lang, code = inline_query.matches[0].group(1, 2)
    request = RunRequest(lang, code, "")
    response = run_code(request)
    if response.result == RESULT_SUCCESS:
        await inline_query.answer([{"title": "Run Code", "description": f"Output: {response.output}", "message_text": f"Output: {response.output}"}])
    elif response.result == RESULT_ERROR:
        await inline_query.answer([{"title": "Run Code", "description": f"Error: {response.output}", "message_text": f"Error: {response.output}"}])
    else:
        await inline_query.answer([{"title": "Run Code", "description": "Unknown error occurred", "message_text": "Unknown error occurred"}])

bot.run()
