import json
import os
from typing import List

import requests
from discord.ext.base.bot import BaseBot
from discord.ext.base.config import config
from dotenv import load_dotenv

from wit import Wit

from Utils.components.approveDeny import ApproveDenyView


class RantBot(BaseBot):
    def __init__(self):
        super().__init__(devMode=False, status=("Caching", "with the devs!"))

        load_dotenv()

        self.wit_client = Wit(self.secure[self.runType]["wit"])

    def get_config(self):
        with open("Configs/config.json", encoding='utf8') as file:
            return json.load(file)

    def get_secure(self):
        with open("Configs/secure.json", encoding='utf8') as file:
            return json.load(file)

    def get_messages_channel(self):
        return self.get_channel(self._config["channels"]["messages"])

    async def _getCogs(self):
        dontLoad = []
        for i in os.listdir('Cogs'):
            if i.endswith('.py') and i not in dontLoad:
                self.initial_extensions.append(f'Cogs.{i[:-3]}')
