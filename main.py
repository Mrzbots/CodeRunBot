from pyrogram import Client, filters
import logging
logging.basicConfig(level=logging.INFO)

bot = Client("bot", api_id=27215224, api_hash="688ae67db37f0ae991c3ecb97d73ff0a", bot_token="7851237202:AAEszK9R4Sr99thXEiQnFbV8K4nFu9Ksjew", plugins=dict(root="bot"))

print("Bot now working 🥰")
bot.run()
