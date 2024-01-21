import bot
import server
import os
import json
import re

# text = re.sub("url", server.site_url(), os.getenv("setup"))
# print(text)
# setup = json.loads(str(text))

server.start()
# bot.run(setup=setup, token=os.getenv("TOKEN"))
