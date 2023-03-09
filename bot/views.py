from discord import ui, ButtonStyle, Interaction, Role

# Define a simple View that gives us a confirmation menu


class ConfirmView(ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @ui.button(label='Confirm', style=ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        await interaction.response.send_message('Confirmed', ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @ui.button(label='Cancel', style=ButtonStyle.grey)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        await interaction.response.send_message('Cancelled', ephemeral=True)
        self.value = False
        self.stop()


class JoinCampaignButton(ui.Button):
    def __init__(self, role: Role = None):
        super().__init__(label='Join This Campaign', style=ButtonStyle.green, custom_id=role.name)
        self.role = role

    async def callback(self, interaction: Interaction):
        await interaction.response.send_message('Campaign Joined', ephemeral=True)
        await interaction.user.add_roles(self.role)


class CampaignButtonView(ui.View):
    def __init__(self, role: Role):
        super().__init__(timeout=None)
        button = JoinCampaignButton(role=role)
        self.add_item(button)
        self.is_persistent = True
