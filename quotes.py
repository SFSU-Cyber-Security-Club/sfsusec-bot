from discord.ext import commands
from datetime import datetime, timedelta
import asyncio
import random

post_time = 86400  # 1 day
file = open('StIGNUcius.txt', 'r')
verses = file.readlines()
quotes = []

# add the lines from the text file to the
for verse in verses:
    if verse[-1] == '\n':
        quotes.append(verse)

async def post_quotes(bot: commands.Bot, general_ID: str):
    '''
    Post a random quote from Richard Stallman everyday from the StIgnucious text file
    '''
    general = bot.get_channel(general_ID)
    while 1 and not len(quotes) == 0:
        now = datetime.now()
        noon = now.replace(hour=12, minute=0, second=0)
        if now >= noon:
            noon += timedelta(days=1)
        await asyncio.sleep((noon-now).total_seconds())
        quote = random.choice(quotes)
        await general.send(f'"{quote.strip()}" - Richard Stallman')
        quotes.remove(quote)
        await asyncio.sleep(post_time)
