from dotenv import load_dotenv

import bot

client = bot.RantBot()

load_dotenv()

client.run(client.getToken())

