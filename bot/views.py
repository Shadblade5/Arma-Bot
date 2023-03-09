from discord import ui, ButtonStyle, Interaction

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

# TRAINING_ROLES = ["Need ACC Cert", "Need Leadership Cert", "Need Transportation Cert"]
# COMPLETED_TRAINING_ROLES = ["ACC", "Leadership", "Transportation"]

# class trainingRoleView(ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)

#     @ui.select(placeholder="Loading...",custom_id="Training Role Selector",
#                     min_values=1,max_values=TRAINING_ROLES.count,options=[
#                 discord.SelectOption(label="Need ACC Cert"),
#                 discord.SelectOption(label="Need Leadership Cert"),
#                 discord.SelectOption(label="Need Transportation Cert"),
#                 ])
#     async def select_callback(self,select,interaction:discord.Interaction):
#         roles = []
#         # for Role in select:
#         #     Role = str(Role)
#         #     CompletedRole = discord.utils.get(interaction.guild.roles, name=Role.split(" ")[2])
#         #     if(interaction.user.roles.index(CompletedRole)!= ValueError):
#         #         interaction.user.add_roles(roles.append(discord.utils.get(interaction.guild.roles, name=Role)))
#         await interaction.response.send_message(f"Roles added! You will recieve a ping when a trainer runs any of the selected roles")
