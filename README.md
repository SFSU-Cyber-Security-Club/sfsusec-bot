**Not Implemented Yet**
HELP (/help)
 - It brings you to the GitHub page's README

VERIFIER (/sfsu_verification: SFSU-email)
 - Input valid SFSU email
 - Recieve a code sent via email
 - Reply to the Bot's DM with the code
 - If correct, you should have the SFSU student role in the server

**Not Implemented Yet**
SECRET TALK (/secret_talk: secret-message)
 - Input your secret message
 - The Bot will use a XOR function to encrypt it (https://en.wikipedia.org/wiki/XOR_cipher)
 - The Bot will DM you the decryption key to share
 - Replying to the encrypted message with the key will decipher it and show you the true message

EVENT REMINDER (automatic)
 - The Bot will check everyday for events
 - For every event, the Bot will start a timer for 5 minutes before the event
 - The reminder will be posted in the announcements chat

DAILY DOSES OF RICHARD STALLMAN QUOTES (automatic)
 - Posts a random quote from St. IGNUcius of the Church of Emacs everyday
 - IDK Michael wanted this for some reason

SETUP (config.ini):
> [DEFAULT]
> token = 
> server_id = 
> announcements_id = 
> general_id = 
> bot_user = 
> bot_pwd = 

REMINDERS
 - Role name must be "SFSU student"
 - Quote & event check timers can only be changed via code (lmk if they need changing)
 - There's only enough quotes for like 3 weeks, more will be added