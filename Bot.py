import asyncio

from main import bot

async def main():
    await bot.run()
    await bot.idle()
    
asyncio.run(main())
