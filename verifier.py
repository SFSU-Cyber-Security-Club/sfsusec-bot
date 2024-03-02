import discord
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# for the code generator
import random

# stores the used codes to prevent repeats
used_codes = []
# the id of the student role
role = 111

async def generate_code():
    '''
    Generate a 5 letter long code to send to their email and save it to verify later
    '''
    code = ''.join(chr(random.randint(48, 57)) if random.choice([True, False]) else chr(random.randint(65, 90)) if random.choice([True, False]) else chr(random.randint(97, 122)) for _ in range(5))
    used_codes.append(code)
    return code

# SOURCE: https://github.com/nbargenda/MessageMailBot
async def send_email(bot, email):
    '''
    Generate the code, compile an email, and send it to the email
    '''
    gmail_user = "@gmail.com"
    gmail_pwd = ""
    FROM = "SFSU Cyber security bot"
    TO = email
    SUBJECT = "Your verification code"
    code = generate_code()
    used_codes.append(code)
    message = f"Here is your verification code: {code} please respond to the bot's direct message."

    print(f"Sending email to {email} with the code: {code}...")
    print("------------------------------------------------------------------------------")

    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = email
    msg.attach(MIMEText(message,'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, msg.as_string())
        server.close()
        print("successfully sent the mail to " + email)
    except: print("failed to send mail to " + email)

    bot.send_message(discord.User, "Please message me the code that was sent to your email...")

# gets called once someone dms the bot back
@bot.event
async def Check_code(msg: str, code: str):
    '''
    if the user responds to a dm check the code pasted with the one saved
    if successful give them the SFSU student role in server
    '''
    if msg.author == bot.user:
        return
    elif msg.content == code:
        if (msg.author.cahce.has(role)):
            await msg.channel.send("You already have the SFSUstudent role!") 
        await msg.channel.send("Success, you have been verified and give the \"SFSU student\" role")
    else:
        await msg.channel.send("Incorrect code! please send me the correct 5 letter code...")