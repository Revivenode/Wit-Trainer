import discord


class ApproveDenyView(discord.ui.View):
    def __init__(self, message, intent, disabled=False):
        super().__init__(timeout=None)

        self.add_item(ApproveButton(message, intent, disabled))
        self.add_item(DenyButton(message, intent, disabled))
        self.add_item(IgnoreButton(disabled, intent, disabled))


class ApproveButton(discord.ui.Button):
    def __init__(self, message, intent, disabled):
        super().__init__(style=discord.ButtonStyle.green, label="Approve", custom_id="approve", disabled=disabled)

        self.message = message
        self.intent = intent

    async def callback(self, interaction: discord.Interaction):
        interaction.client.wit_client.train([{"text": self.message, "intent": self.intent, "entities": [], "traits": []}])
        await interaction.message.edit(content=f'*{self.message}*\n\n`{self.intent}`\n\nApproved', view=ApproveDenyView(self.message, self.intent, True))


class DenyButton(discord.ui.Button):
    def __init__(self, message, intent, disabled):
        super().__init__(style=discord.ButtonStyle.red, label="Deny", custom_id="deny", disabled=disabled)

        self.message = message
        self.intent = intent

    async def callback(self, interaction: discord.Interaction):
        interaction.client.wit_client.train([{"text": self.message, "entities": [], "traits": []}])
        await interaction.message.edit(content=f'*{self.message}*\n\n`{self.intent}`\n\nDenied', view=ApproveDenyView(self.message, self.intent, True))


class IgnoreButton(discord.ui.Button):
    def __init__(self, message, intent, disabled):
        super().__init__(style=discord.ButtonStyle.gray, label="Ignore", custom_id="ignore", disabled=disabled)

        self.message = message
        self.intent = intent

    async def callback(self, interaction: discord.Interaction):
        await interaction.message.edit(content=f'*{self.message}*\n\n`{self.intent}`\n\nIgnored', view=ApproveDenyView(self.message, self.intent, True))
