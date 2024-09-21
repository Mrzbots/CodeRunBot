from settings import LANGS
from main import bot

@bot.on_message(filters.command("langs"))
async def langs(client, message):
    await message.reply_text(LANGS)
