from discord.ext import commands
import asyncio
import random

post_time = 86400 # 1 day 
file = open("StIGNUcius.txt", "r")
verses = file.readlines()
quotes = []

for verse in verses:
    if verse[-1] == "\n":
        quotes.append(verse)
        
# checks every hour post a quote from Richard Stallman
async def post_quotes(bot: commands.Bot, general_ID: str):
     general = bot.get_channel(general_ID)
     while 1:
        quote = random.choice(quotes)
        await general.send(f"\"{quote.strip()}\" - Richard Stallman")
        quotes.remove(quote)
        await asyncio.sleep(post_time)