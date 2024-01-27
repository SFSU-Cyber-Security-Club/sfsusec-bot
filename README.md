Functionalities (main):
 - Posts a reminder in the announcements page when an event begins
 - Confirms SFSU identity
   - Bot will ask for an SFSU email (will reply with a negative response if not SFSU domain)
   - Sends a code to that email
   - Requests for that code in DMs to confirm Identity
   - Gives "SFSU student" role in server for proof of verification
Functionalities (secondary):
 - Secret speak (https://en.wikipedia.org/wiki/XOR_cipher)
   - Bot will take in message and XOR it
   - Bot will DM the key to share
   - If a user replies to the message with the correct cipher, show the hidden message
 - Posts random Richard Stallman quotes in general for whatever reason

TODO:
 - Implement emailing and DM functionalities of the verification command
 - Implement the encypting function for secret talk
 - Find some Richard Stallman quotes