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
    print(f'sending email to {email} with the code: {code}\n')
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
        print(f'successfully sent the mail to {email}\n')
        return None
    except smtplib.SMTPException as e:
        if 'Daily user sending limit exceeded' in str(e):
            err_msg = 'Email sending limit reached for the day'
        else:
            err_msg = 'Failed to send email, please contact an Officer about the issue'
        print(f'failed to send email to {email}: {e}\n')
        return err_msg

# gets called once someone dms the bot back
# https://stackoverflow.com/questions/48987006/how-to-make-a-discord-bot-that-gives-roles-in-python
async def check_code(bot: commands.Bot, server_ID: int, msg: discord.Message):
    '''
    - Bot checks DMs for response to the prompt
    - Compare the msg to the UID:code pair for verification
    - If successful give them the SFSU student role in server
    '''
    print(f'{msg.author} texted: {msg.content} --- code saved for {msg.author}: {codes[msg.author.id]}\n')
    if msg.content.strip() == codes[msg.author.id].strip():
        try: 
            guild = bot.get_guild(server_ID)
            role = get(guild.roles, name='SFSU student')
            member = await guild.fetch_member(msg.author.id)
            await member.add_roles(role)
            print(f'successfully granted {msg.author} the SFSU-student role\n')
            await msg.author.send('Success! You have been granted the **SFSU student** role!')
            return 0
        except discord.Forbidden as e:
            print(f'ERROR: permission error: {e}\n')
            await msg.author.send('Sorry, I lack the permission to give you this role, please contact an Officer to fix this.')
            return 1
        except discord.HTTPException as e:
            print(f'ERROR: some error: {e}\n')
            await msg.author.send('Sorry, an error has occured that should not have, please contact an Officer to fix this')
            return 1
    else:
        print('the code was incorrect...\n')
        await msg.author.send('Sorry, the code you have sent was not correct...')
        return 1
