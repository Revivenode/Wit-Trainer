from dotenv import load_dotenv

import bot

client = bot.RantBot()

client.run(client.getToken())

