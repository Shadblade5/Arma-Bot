import discord
from discord.ext import commands
import config
from database import Database
import random

description = '''Here are the following commands available.'''

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config.c.prefix, description=description, intents=intents)
DB = Database(config.c.db_host,config.c.db_username,config.c.db_password,"br1")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the server burn"))

@bot.event
async def on_member_join(ctx):
    DB.adduser(ctx.id,ctx.name)

@bot.command()
async def getusers(ctx):
    await ctx.send(DB.getUsers())

@bot.command()
async def getuserinfo(ctx):
    userinfo = DB.getUserInfo(ctx.author.id)
    response = " Name: {0}\nDiscordID: {1}\nGrade: {2}\nJoinDate: {3}\nBirthday: {4}".format(userinfo[1],userinfo[0],userinfo[2],userinfo[4],userinfo[5])
    await ctx.send(response)


@bot.command()
async def adduser(ctx):
    """Adds user to database"""
    view = Confirm()
    await ctx.send('Do you want to continue?', view=view)
    # Wait for the View to stop listening for input...
    await view.wait()
    if view.value is None:
        await ctx.send('Timed out...')
    elif view.value:
        if DB.adduser(ctx.author.id, ctx.author.name):
            await ctx.send('Confirmed... adding user.')
        else:
            await ctx.send("User failed to be added to the database.")
    else:
        await ctx.send('Cancelled...user was not added.')

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    embed = discord.Embed(title='Reloaded', description=f'{extension} successfully reloaded!', color=0xff00c8)
    await ctx.send(embed=embed)

@bot.command()
async def setbirthday(ctx,month,day,year):
    birthday = "{0}-{1}-{2}".format(month,day,year)
    await ctx.send(birthday)
    DB.setBirthday(ctx.author.id,birthday)

# Define a simple View that gives us a confirmation menu
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Confirmed', ephemeral=False)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelled', ephemeral=False)
        self.value = False
        self.stop()


bot.run(config.c.token)

