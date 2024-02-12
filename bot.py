import discord
from discord import app_commands
from discord.ext import commands
import asyncio

from reminder import event_check
from quotes import post_quotes
from verifier import send_email 

# settings
Token = ""
# copy channel ID
announcements_ID = 1
general_ID = 1
# copy server ID
server_ID = 1 

bot = commands.Bot(command_prefix='', intents=discord.Intents.default())

# start
@bot.event
async def on_ready():
    print("Initializing variables and syncing commands...")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commands have been synced!")
    except Exception as e:
        print(e)
    guild = bot.get_guild(server_ID)
    announcements = bot.get_channel(announcements_ID)
    general = bot.get_channel(general_ID)
    # ensure variables are properly initialized
    await asyncio.sleep(3)
    print(f"{bot.user} is now running!")
    asyncio.create_task(event_check(bot, guild, announcements))
    asyncio.create_task(post_quotes(general))

# test slash command
@bot.tree.command(name="test", description="this is a test command to ensure slash commands are working")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message(f"Yup, seems okay...", ephemeral=True)

# SFSU Verification
@bot.tree.command(name="sfsu_verification", description="Gain the \"SFSU student\" role by verifying your valid SFSU email")
@app_commands.describe(email = "Enter email address")
async def verification(interaction: discord.Interaction, email: str): 
    '''
    - Bot will ask for an SFSU email (will reply with a negative response if not SFSU domain)
    - Sends a code to that email
    - Requests for that code in DMs to confirm Identity
    - Gives "SFSU student" role in server for proof of verification
    '''
    if email[-8:] != "sfsu.edu":
        await interaction.response.send_message(f"Not a valid SFSU email", ephemeral=True)
        return
    dm = await interaction.user.create_dm()
    await dm.send("Please reply here with the code sent to your email")
    asyncio.create_task(send_email(email))
    await interaction.response.send_message(f"A code has been sent to {email}, please DM that code for confirmation", ephemeral=True)

# Secret talk
@bot.tree.command(name="secret_talk", description="Encrypt your message with a key you can share!")
@app_commands.describe(msg = "Enter secret message")
async def Secret_talk(interaction: discord.Interaction, msg: str): 
    '''
    - Bot will take in message and XOR it
    - Bot will DM the key to share
    - If a user replies to the message with the correct cipher, show the hidden message
    '''
    encrypted = "ecnrypt the msg"
    await interaction.response.send_message(f"{interaction.user.name} says: {encrypted}")

bot.run(Token)