import asyncio
import random

post_time = 3600 # 1 hr
quotes = ["some",
          "stuff",
          "Richard",
          "Stallman",
          "said"]

# checks every hour post a quote from Richard Stallman
async def post_quotes(bot, general):
    while 1:
        await general.send(f"\"{random.choice(quotes)}\" - Richard Stallman")
        await asyncio.sleep(post_time)