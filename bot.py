import asyncio
from main import bot

async def main():
    await bot.start()
    print(f"{bot.mention} working 🔥")

asyncio.run(main())
