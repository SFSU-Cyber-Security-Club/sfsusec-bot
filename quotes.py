import asyncio
import random

post_time = 86400 # 1 day 
quotes = ["In the US, you even lose legal rights if you store your data in a company's machines instead of your own. The police need to present you with a search warrant to get your data from you; but if they are stored in a company's server, the police can get it without showing you anything.",
          "People sometimes ask me if it is a sin in the Church of Emacs to use vi. Using a free version of vi is not a sin; it is a penance. So happy hacking.",
          "The idea of free software is that users of computing deserve freedom. They deserve in particular to have control over their computing. And proprietary software does not allow users to have control of their computing.",
          "If you install ubuntu, you're in big trouble",
          "To GNU or be GNU'ed, that is the question",
          "Haha i amm richard stallman i am awesome ",
          "When I launched the development of the GNU system, I explicitly said the purpose of developing this system is so we can use our computers and have freedom, thus if you use some other free system instead but you have freedom, then it's a success. It's not popularity for our code but it's success for our goal.",
          "In essence, Chrome OS is the GNU/Linux operating system. However, it is delivered without the usual applications, and rigged up to impede and discourage installing applications.",
          "Android is very different from the GNU/Linux operating system because it contains very little of GNU. Indeed, just about the only component in common between Android and GNU/Linux is Linux, the kernel.",
          "Proprietary software keeps users divided and helpless. Divided because each user is forbidden to redistribute it to others, and helpless because the users can't change it since they don't have the source code. They can't study what it really does. So the proprietary program is a system of unjust power.",
          "All governments should be pressured to correct their abuses of human rights."]

# checks every hour post a quote from Richard Stallman
async def post_quotes(general):
    while 1:
        await general.send(f"\"{random.choice(quotes)}\" - Richard Stallman")
        await asyncio.sleep(post_time)