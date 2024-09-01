import discord
import asyncio
from discord import app_commands
from discord.ext import commands
from configparser import ConfigParser

from reminder import event_check
from quotes import post_quotes
from verifier import send_email
from verifier import check_code

bot = commands.Bot(command_prefix='', intents=discord.Intents.default())
intents = discord.Intents.default()
config = ConfigParser()
config.read("config.ini")
data = config["DEFAULT"]

# settings
Token = data["token"]
server_ID = int(data["server_ID"])
announcements_ID = int(data["announcements_ID"])
general_ID = int(data["general_ID"])
bot_user = data["bot_user"]
bot_pwd = data["bot_pwd"]

# start
@bot.event
async def on_ready():
    print("Initializing variables and syncing commands...")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commands have been synced!")
    except Exception as e:
        print(e)
    # ensure variables are properly initialized
    await asyncio.sleep(3)
    print(f"{bot.user} is now running!")
    asyncio.create_task(event_check(bot, server_ID, announcements_ID))
    asyncio.create_task(post_quotes(bot, general_ID))

@bot.event
async def on_message(msg: discord.Message):
    asyncio.create_task(check_code(bot, server_ID, msg))

# help
@bot.tree.command(name="help", description="all commands with their functionalities")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message("help", ephemeral=True)

# SFSU Verification
@bot.tree.command(name="sfsu_verification", description="Gain the \"SFSU student\" role by verifying your valid SFSU email")
@app_commands.describe(email = "Enter SFSU email")
async def verification(interaction: discord.Interaction, email: str): 
    '''
    - Bot will ask for an SFSU email (will reply with a negative response if not SFSU domain)
    - Sends a code to that email
    - Requests for that code in DMs to confirm Identity
    - Gives "SFSU student" role in server for proof of verification
    '''
    if not email.endswith("@sfsu.edu") or email.endswith("@mail.sfsu.edu"):
        await interaction.response.send_message(f"Not a valid SFSU email", ephemeral=True)
        return
    dm = await interaction.user.create_dm()
    asyncio.create_task(send_email(email, interaction.user.id, bot_user, bot_pwd))
    await dm.send("Please reply here with the code sent to your email")
    await interaction.response.send_message(f"A code has been sent to **{email}**, please DM that code for confirmation", ephemeral=True)

# secret talk
@bot.tree.command(name="secret_talk", description="Encrypt your message with a key you can share!")
@app_commands.describe(msg = "Enter secret message")
async def Secret_talk(interaction: discord.Interaction, msg: str): 
    '''
    - Bot will take in message and XOR it
    - Bot will DM the key to share
    - If a user replies to the message with the correct cipher, show the hidden message
    '''
    encrypted = "encrypt the msg"
    await interaction.response.send_message(f"{interaction.user.name} says: {encrypted}")

bot.run(Token)