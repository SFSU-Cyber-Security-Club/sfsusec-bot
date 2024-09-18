import discord
import smtplib
import random

from discord.ext import commands
from discord.utils import get
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

codes = {}  # tracks used codes and UIDs that go with them

async def generate_code():
    '''
    Generates a random 5 letter/digit code
    '''
    code = ''.join((chr(random.randint(48, 57))if random.choice([True, False])else(chr(random.randint(65, 90))if random.choice([True, False])else chr(random.randint(97, 122))))for _ in range(5))
    return code

# generate the code, compile an email, and send it to the email
# SOURCE: https://github.com/nbargenda/MessageMailBot
async def send_email(email: str, uid: str, bot_user: str, bot_pwd: str):
    '''
    Sends an email to the address from the bot email using SMTP
    '''
    username = bot_user
    password = bot_pwd
    FROM = username
    TO = email
    SUBJECT = 'Your verification code'
    code = await generate_code()
    codes[uid] = code
    file = open('codes.txt', 'a')
    file.write(f'{uid} : {code}\n')
    message = 'Here is your verification code: ' + code
    print(f'sending email to {email} with the code: {code}')
    print('------------------------------------------------------------------------------')
    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = email
    msg.attach(MIMEText(message, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(FROM, TO, msg.as_string())
        server.close()
        print(f'successfully sent the mail to {email}')
    except Exception as e:
        print(f'failed to send email to {email}: {e}')

# gets called once someone dms the bot back
# https://stackoverflow.com/questions/48987006/how-to-make-a-discord-bot-that-gives-roles-in-python
async def check_code(bot: commands.Bot, server_ID: int, msg: discord.Message):
    '''
    - Bot checks DMs for response to the prompt
    - Compare the msg to the UID:code pair for verification
    - If successful give them the SFSU student role in server
    '''
    print(f'message-{msg.content} : saved-{codes[msg.author.id]}')
    if msg.content == codes[msg.author.id]:
        guild = bot.get_guild(server_ID)
        role = get(guild.roles, name='SFSU student')
        member = await guild.fetch_member(msg.author.id)
        await member.add_roles(role)
        await msg.author.send('Success! You have been granted the **SFSU student** role!')
        return 0
    else:
        await msg.author.send('Sorry, the code you have sent was not correct...')
        return 1
