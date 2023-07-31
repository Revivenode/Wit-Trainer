import discord
from discord.ext import commands

from Utils.components.approveDeny import ApproveDenyView


class WitAI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener(name="on_message")
    async def confidence(self, message):
        if message.guild.id != self.client._config["main_guild"]:
            return

        if message.channel.id == self.client._config["channel"]:
            return

        if discord.utils.get(message.guild.roles, id=self.client._config["staff"]) in message.author.roles:
            return

        response = self.client.wit_client.message(message.content, n=1)

        if len(response["intents"]) == 0:
            return

        intent = response["intents"][0]

        if intent["confidence"] > self.client._config["confidence"]:
            utterances = self.client.wit_client.get_utterances(10000, intents=[intent["name"]])
            flag = True
            for utterance in utterances:
                if utterance["text"] == message.content:
                    flag = False
                    break

            if flag:
                channel = self.client.get_channel(self.client._config["channel"])
                await channel.send(f'Should *{message.content}* trigger the intent `{intent["name"]}`?\n\nConfidence: {intent["confidence"]*100:2f}%', view=ApproveDenyView(message.content, intent["name"]))


async def setup(client):
    await client.add_cog(WitAI(client))
