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

        interaction.client.logger.info(f'{interaction.user} approved {self.message} for {self.intent} with {self.confidence}')
        await interaction.response.edit_message(content=f'Message: `{self.message}`\n\nIntent: `{self.intent}`\n\nConfidence: `{self.confidence}`\n\nApproved by {interaction.user.mention}', view=ApproveDenyView(self.message, self.intent, self.confidence, True, self.testing))


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

        interaction.client.logger.info(f'{interaction.user} denied {self.message} for {self.intent} with {self.confidence}')
        await interaction.response.edit_message(content=f'Message: `{self.message}`\n\nIntent: `{self.intent}`\n\nConfidence: `{self.confidence}`Denied by {interaction.user.mention}', view=ApproveDenyView(self.message, self.intent, self.confidence, True, self.testing))


class IgnoreButton(discord.ui.Button):
    def __init__(self, message, intent, confidence, disabled, testing):
        super().__init__(style=discord.ButtonStyle.gray, label="Ignore", custom_id="ignore", disabled=disabled)

        self.message = message
        self.intent = intent
        self.confidence = confidence
        self.testing = testing

    async def callback(self, interaction: discord.Interaction):
        interaction.client.logger.info(f'{interaction.user} ignored {self.message} for {self.intent} with {self.confidence}')
        await interaction.response.edit_message(content=f'Message: `{self.message}`\n\nIntent: `{self.intent}`\n\nConfidence: `{self.confidence}`Ignored by {interaction.user.mention}', view=ApproveDenyView(self.message, self.intent, self.confidence, True, self.testing))
