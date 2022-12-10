import discord
from discord.ext import commands
import config
from database import Database
import random
import datetime
import pytz
import time

description = '''Here are the following commands available.'''

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config.c.prefix, description=description, intents=intents)
DB = Database(config.c.db_host,config.c.db_username,config.c.db_password,"br1")

@bot.event
async def on_ready():
    print('Logged in as')
    output = bot.user.name + " ID:" + str(bot.user.id)
    print(output)
    print('-'*len(output))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the server burn"))


async def playerlogger(ctx):
    channel = bot.get_channel(1049510076945281086)
    timestamp = ctx.message.created_at.astimezone(pytz.timezone('US/Eastern'))
    em = discord.Embed()
    em.set_thumbnail(url=ctx.author.display_avatar.url)
    em.thumbnail.width = 20
    em.thumbnail.height = 20
    em.title="{}#{}".format(ctx.author.name,ctx.author.discriminator)
    em.add_field(name="Command Used",value=ctx.command)
    Args = ctx.message.content.split(bot.command_prefix + ctx.command.name + " ")
    if(len(Args)>1):
        em.add_field(name="Arguments", value=Args[1],inline=False)
    em.set_footer(text="{}".format(timestamp.strftime("%Y-%m-%d at %I:%M:%S %p %Z")))
    em.colour=discord.Colour.blue()
    await channel.send(embed=em)

@bot.event
async def on_member_join(ctx):
    await DB.adduser(ctx.id,ctx.name)

@bot.command()
async def getusers(ctx):
    await ctx.send(await DB.getUsers())

@bot.command()
async def getuserinfo(ctx):
    message = await ctx.send("Getting user info...")
    userinfo = await DB.getUserInfo(ctx.author.id)
    await message.edit(content="Name: {0}\nDiscordID: {1}\nGrade: {2}\nJoinDate: {3}\nBirthday: {4}"
                   .format(userinfo[1],userinfo[0],userinfo[2],userinfo[4],userinfo[5]))

@bot.command()
async def id(ctx, *args):
    # targetusers.append(user.id for user in ctx.message.mentions
    # test = "208119044308467712"
    # for x in "<@>":
    #     test = test.replace(x,"")
    # print(test)
    # if len(args)>1:
    targetUsers = []
    print(args)
    for x in args:
        for y in "<@>&":
            x = x.replace(y,"")
        targetUsers.append(x)
    print(targetUsers)

# @bot.command()
# async def updateCoC(ctx):
#     channel = bot.get_channel(1050527640848695296)

@bot.command()
async def createcoc(ctx):
    channel = bot.get_channel(1049510076945281086)
    coc = await DB.getcoc()

    print(coc)




    # dir = "./CoC Documents/"
    # f1 = open("./CoC Documents/PREAMBLE.txt", "r")
    # em = discord.Embed()
    # em.title = "PREAMBLE"
    # em.description = f1.read()
    # f1.close()
    # await ctx.send(embed=em)
    #
    # for x in ["DEFINITIONS",
    #           "GENERAL CONDUCT",
    #           # "OPERATIONAL CONDUCT",
    #           # "CAMPAIGN OPERATION AND MODLISTS DESIGN",
    #           # "CAMPAIGN AND OPERATION SIGNUP",
    #           # "ADMINISTRATIVE DUTIES",
    #           # "DISCIPLINE"
    #           ]:
    #     message = await channel.send(content=x)
    #     thread = await message.create_thread(name=x)
    #     em2 = discord.Embed()
    #     f2 = open(dir + x+".txt", "r")
    #     em2.description = f2.read()
    #     f2.close()
    #     await thread.send(embed=em2)

@bot.command()
@commands.has_any_role('Officer', 'Admin-NCO','Senior-NCO')
@commands.cooldown(1,60,commands.BucketType.guild)
@commands.max_concurrency(1,per =commands.BucketType.guild,wait=True)
@commands.after_invoke(playerlogger)
async def adduser(ctx,*args):
    """Adds user to the database"""
    view = Confirm()
    await ctx.send('Confirmation to add {} to the database', view=view)
    # Wait for the View to stop listening for input...
    await view.wait()
    if view.value is None:
        await ctx.send('Timed out...')
    elif view.value:
        if (await DB.adduser(ctx.author.id, ctx.author.name)):
            await ctx.send('Confirmed, adding user...')
        else:
            await ctx.send("User already exists in the database.")
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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.UserInputError):
        await ctx.send(error)
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Command on Cooldown", description=f"Try again in {error.retry_after:.2f}s.",
                           color=discord.Colour.red())
        await ctx.send(embed=em)


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
        await interaction.response.send_message('Confirmed', ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelled', ephemeral=True)
        self.value = False
        self.stop()


bot.run(config.c.token)

