import discord
import asyncio

from configparser import ConfigParser
from discord import app_commands
from discord.ext import commands
from quotes import post_quotes
from reminder import event_check
from verifier import check_code, send_email
from cipher import generate_key, xor_cipher, xor_decipher

bot = commands.Bot(command_prefix='', intents=discord.Intents.default())
needs_verification = {}
intents = discord.Intents.default()
config = ConfigParser()
config.read('config.ini')
data = config['DEFAULT']

# settings
Token = data['token']
server_ID = int(data['server_ID'])
announcements_ID = int(data['announcements_ID'])
general_ID = int(data['general_ID'])
bot_user = data['bot_user']
bot_pwd = data['bot_pwd']

# start
@bot.event
async def on_ready():
    print('Initializing variables and syncing commands...')
    try:
        synced = await bot.tree.sync()
        print(f'{len(synced)} commands have been synced')
    except Exception as e:
        print(e)
    await asyncio.sleep(3) # ensure variables are properly initialized 
    print(f'{bot.user} is now running!\n')
    asyncio.create_task(event_check(bot, server_ID, announcements_ID))
    asyncio.create_task(post_quotes(bot, general_ID))

# print help
@bot.tree.command(name='help', description='All commands with their functionalities')
async def help(interaction: discord.Interaction):
    with open('README.md', 'r') as f:
        content = f.read()
    await interaction.response.send_message(content, ephemeral=True)

# SFSU Verification
@bot.tree.command(name='sfsu-verification', description='Gain the SFSU student role by verifying your valid SFSU email')
@app_commands.describe(email='Enter SFSU email')
async def verification(interaction: discord.Interaction, email: str):
    '''
    - Bot will ask for an SFSU email (will reply with a negative response if not SFSU domain)
    - Sends a code to that email
    - Requests for that code in DMs to confirm Identity
    - Gives 'SFSU student' role in server for proof of verification
    '''
    if not email.endswith('@sfsu.edu') or email.endswith('@mail.sfsu.edu'):
        await interaction.response.send_message('Not a valid SFSU email', ephemeral=True)
        return
    await interaction.response.defer() # in case sending the email takes more than 3 seconds
    dm = await interaction.user.create_dm()
    err_msg = await send_email(email, interaction.user.id, bot_user, bot_pwd)
    if err_msg is None:
        needs_verification[interaction.user.id] = True
        await dm.send(f'Please reply here with the code sent to **{email}**')
        await interaction.followup.send(f'A code has been sent to your email, please DM that code for confirmation')
    else:
        await interaction.followup.send(f'There was a problem sending the email: {err_msg}')

# checks for code in DMs
@bot.event
async def on_message(msg: discord.Message):
    if not isinstance(msg.channel, discord.DMChannel) or msg.author.id==bot.user.id:
        return
    if msg.author.id in needs_verification:
        check = await check_code(bot, server_ID, msg) 
        if (check == 0):
            del needs_verification[msg.author.id]
    else:
        await msg.author.send('There is no code under your ID right now, please use the /sfsu-verification command here or in the server')

# secret talk
@bot.tree.command(name='secret-talk', description='Encrypt your message with a key you can share')
@app_commands.describe(msg='Enter secret message')
async def secret_talk(interaction: discord.Interaction, msg: str):
    '''
    - Bot will take message, cipher it, and save the key
    - The key will be DM'd to the user
    - The encrypted message will be published in the same channel
    '''
    key = await generate_key()
    cipher = await xor_cipher(msg, key)
    channel = bot.get_channel(interaction.channel_id)
    await channel.send(f'**{interaction.user.name} says:** {cipher}')
    await interaction.response.send_message(f'Here is your cipher key (**{key}**) share with caution 🤫🔑', ephemeral=True)

# decipher
@bot.tree.command(name='decrypt-cipher', description='Reply to a cipher with the key to decrypt it')
@app_commands.describe(cipher='Enter ciphered text', key='Enter cipher key')
async def decrypt_cipher(interaction: discord.Interaction, cipher: str, key: str):
    '''
    - Bot will take in encrypted message and key
    - The message will be deciphered and privatley shown to the user in the same channel
    '''
    deciphered = await xor_decipher(cipher, key)
    await interaction.response.send_message(f'(**{key}**) {deciphered}', ephemeral=True)
bot.run(Token)
