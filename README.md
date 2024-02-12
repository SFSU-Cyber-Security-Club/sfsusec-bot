*NEW*
- Added the EMAILING & DMING capabilities for the SFSU email authenticator
- Added Richard Stallman quotes (and increased the time to ONE post per day)

TODO:
 - Implement the actual verification process
 - Create an "SFSU student" role
 - Implement the encypting function for secret talk

Functionalities (main):
 - Posts a reminder in the announcements page when an event begins
 - Authenticate SFSU users via email
   - Bot will ask for an SFSU email (will reply with a negative response if not SFSU domain)
   - Sends a code to that email
   - Requests for that code in DMs to confirm identity
   - Gives "SFSU student" role in server for proof of verification
Functionalities (secondary):
 - Secret speak (https://en.wikipedia.org/wiki/XOR_cipher)
   - Bot will take in message and XOR it
   - Bot will DM the key to the writer for sharing
   - If a user replies to the encrypted message with the correct cipher, show the hidden message to the key holder
 - Posts random Richard Stallman quotes everyday in general for whatever reason

SETUP:
 - bot.py
   1. valid Token
   2. announcements channel ID
   3. general channel ID
   3. server ID
 - verifier.py
   1. gmail username
   2. gmail password