import asyncio

from main import bot

async def main():
    await bot.start()
    await bot.idle()

asyncio.run(main())
