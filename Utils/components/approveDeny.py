import discord


class ApproveDenyView(discord.ui.View):
    def __init__(self, message, intent, confidence, disabled=False, testing=False):
        super().__init__(timeout=None)

        self.add_item(ApproveButton(message, intent, confidence, disabled, testing))
        self.add_item(DenyButton(message, intent, confidence, disabled, testing))
        self.add_item(IgnoreButton(message, intent, confidence, disabled, testing))


class ApproveButton(discord.ui.Button):
    def __init__(self, message, intent, confidence, disabled, testing):
        super().__init__(style=discord.ButtonStyle.green, label="Approve", custom_id="approve", disabled=disabled)

        self.message = message
        self.intent = intent
        self.confidence = confidence
        self.testing = testing

    async def callback(self, interaction: discord.Interaction):
        if not self.testing:
            interaction.client.wit_client.train([{"text": self.message, "intent": self.intent, "entities": [], "traits": []}])
        await interaction.response.edit_message(content=f'*{self.message}*\n\n`{self.intent}`\n\n`{self.confidence}`\n\nApproved by {interaction.user.mention}', view=ApproveDenyView(self.message, self.intent, self.confidence, True, self.testing))


class DenyButton(discord.ui.Button):
    def __init__(self, message, intent, confidence, disabled, testing):
        super().__init__(style=discord.ButtonStyle.red, label="Deny", custom_id="deny", disabled=disabled)

        self.message = message
        self.intent = intent
        self.confidence = confidence
        self.testing = testing

    async def callback(self, interaction: discord.Interaction):
        if not self.testing:
            interaction.client.wit_client.train([{"text": self.message, "entities": [], "traits": []}])
        await interaction.response.edit_message(content=f'*{self.message}*\n\n`{self.intent}`\n\n`{self.confidence}`\n\nDenied by {interaction.user.mention}', view=ApproveDenyView(self.message, self.intent, self.confidence, True, self.testing))


class IgnoreButton(discord.ui.Button):
    def __init__(self, message, intent, confidence, disabled, testing):
        super().__init__(style=discord.ButtonStyle.gray, label="Ignore", custom_id="ignore", disabled=disabled)

        self.message = message
        self.intent = intent
        self.confidence = confidence
        self.testing = testing

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content=f'*{self.message}*\n\n`{self.intent}`\n\n`{self.confidence}`\n\nIgnored', view=ApproveDenyView(self.message, self.intent, self.confidence, True, self.testing))
