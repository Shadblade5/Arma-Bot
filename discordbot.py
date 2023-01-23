import discord
from discord.ext import commands
from discord.ext import tasks
import config
from database import Database
import random
import datetime
import pytz
import time
import os
import sys
from wakeonlan import send_magic_packet

description = '''Here are the following commands available.'''

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config.c.prefix, description=description, intents=intents)
DB = Database(config.c.db_host, config.c.db_username, config.c.db_password, "arma")


@bot.event
async def on_ready():
    print('Logged in as')
    output = bot.user.name + " ID:" + str(bot.user.id)
    print(output)
    print('-' * len(output))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the server burn"))
    # checkforrestart.start()
    await bot.get_channel(1049510076945281086).send("Bot started.")

async def playerlogger(ctx):
    timestamp = ctx.message.created_at.astimezone(pytz.timezone('US/Eastern'))
    em = discord.Embed()
    em.set_thumbnail(url=ctx.author.display_avatar.url)
    em.thumbnail.width = 20
    em.thumbnail.height = 20
    em.title = "{}#{}".format(ctx.author.name, ctx.author.discriminator)
    em.add_field(name="Command Used", value=ctx.command)
    Args = ctx.message.content.split(bot.command_prefix + ctx.command.name + " ")
    if (len(Args) > 1):
        em.add_field(name="Arguments", value=Args[1], inline=False)
    em.set_footer(text="{}".format(timestamp.strftime("%Y-%m-%d at %I:%M:%S %p %Z")))
    em.colour = discord.Colour.blue()
    await bot.get_channel(1049510076945281086).send(embed=em)


@bot.event
async def on_member_join(ctx):
    await DB.adduser(ctx.id, ctx.name)


@bot.command()
async def getusers(ctx):
    await ctx.send(await DB.getUsers())


@bot.command()
async def getuserinfo(ctx):
    message = await ctx.send("Getting user info...")
    userinfo = await DB.getUserInfo(ctx.author.id)
    await message.edit(content="Name: {0}\nDiscordID: {1}\nGrade: {2}\nJoinDate: {3}\nBirthday: {4}"
                       .format(userinfo[1], userinfo[0], userinfo[2], userinfo[4], userinfo[5]))


# @bot.command()
# async def id(ctx, *args):
# targetusers.append(user.id for user in ctx.message.mentions
# test = "208119044308467712"
# for x in "<@>":
#     test = test.replace(x,"")
# print(test)
# if len(args)>1:
# targetUsers = []
# # print(args)
# for x in args:
#     for y in "<@>&":
#         x = x.replace(y,"")
#     targetUsers.append(x)
# print(targetUsers)

# @bot.command()
# async def updateCoC(ctx):
#     channel = bot.get_channel(1050527640848695296)

class COC:
    em = 0
    thread = 0

    def __init__(self, code):
        self.Section = code[0]
        self.Subsection = code[1]
        self.Item = code[2]
        self.Title = code[3]
        self.Description = code[4]


@bot.command()
async def createcoc(ctx):
    channel = bot.get_channel(1053239585838215229)  # new-code-of-conduct
    print("Getting COC DATA")
    threads = []
    coc = await DB.getcoc()
    # sorted_coc = sorted(
    #     coc,
    #     key=lambda t: (t[0], t[1], t[2])
    # )
    for code in coc:
        # print('{}.{}.{} {}'.format(*code))

        current_code = COC(list(code))
        # print(f'Current: {current_code.Section}.{current_code.Subsection}.{current_code.Item}')

        if (current_code.Section == 0):
            if (current_code.Subsection == 0):
                current_code.em = discord.Embed()
                current_code.em.title = current_code.Title
                current_code.em.description = current_code.Description
                await channel.send(embed=current_code.em)
            else:
                if (current_code.Item == 0):
                    message = await channel.send(embed=discord.Embed(title=current_code.Title))
                    definitions_thread = await message.create_thread(name=current_code.Title)
                else:
                    await definitions_thread.send(
                        embed=discord.Embed(title=current_code.Title, description=current_code.Description))
        else:
            if (current_code.Subsection == 0):
                message = await channel.send(embed=discord.Embed(
                    title=f'{current_code.Section}.{current_code.Subsection}.{current_code.Item} {current_code.Title}'))
                current_thread = await message.create_thread(name=current_code.Title)
            else:
                if current_code.Item == 0:
                    current_code.em = discord.Embed()
                    current_code.em.title = f'{current_code.Section}.{current_code.Subsection}.{current_code.Item} {current_code.Title}'
                    current_code.em.description = current_code.Description
                    if current_code.Subsection > 1:
                        await current_thread.send(embed=last_code.em)
                else:
                    current_code.em = last_code.em
                    current_code.em.add_field(name=current_code.Title, value=current_code.Description, inline=False)

        last_code = current_code


@bot.command()
@commands.has_any_role('Officer', 'Admin-NCO')
async def startserver(ctx):
    await ctx.send("Starting server...")
    send_magic_packet('E0-D5-5E-28-75-DE')

@bot.command()
@commands.is_owner()
async def restartbot(ctx):
    await ctx.send("Bot restarting...")
    await bot.get_channel(1049510076945281086).send("Bot restarting...")
    os.execv(sys.executable, ['python'] + sys.argv)
    sys.exit()
    # f = open("restartflag.txt","r")
    # if(f.readline(1) == "1"):
    #     f.close()
    #     f = open("restartflag.txt","w")
    #     f.write("0")
    #     f.close()

@bot.command()
@commands.has_any_role('Officer','Director',"Assistant Director")
@commands.after_invoke(playerlogger)
async def rankup(ctx, member: discord.Member):
    myguild = ctx.guild
    guildroles = await myguild.fetch_roles()
    memberRoles = member.roles
    oldGrade = "none"
    for role in memberRoles:
        if ("Unit Grade" in role.name):
            oldRole = role
            oldGrade = role.name
            oldgradeNumber = [int(i) for i in oldGrade.split() if i.isdigit()][0]
            oldGradeID = role.id
    if (oldGrade == "none"):
        await ctx.send("Error! {} doesn't have a unit grade".format(member.name))
    else:
        # oldRole = discord.utils.get(ctx.guild.roles, name="Unit Grade {}".format(oldgradeNumber))
        newRole = discord.utils.get(ctx.guild.roles, name="Unit Grade {}".format(oldgradeNumber + 1))

        await member.add_roles(newRole, reason="Rankup")
        await member.remove_roles(oldRole, reason="Rankup")

        await ctx.send("{} ranked up to Unit Grade {}".format(member.name, oldgradeNumber + 1))


@bot.command()
@commands.has_any_role('Officer', 'Admin-NCO', 'Senior-NCO')
@commands.cooldown(1, 60, commands.BucketType.guild)
@commands.max_concurrency(1, per=commands.BucketType.guild, wait=True)
@commands.after_invoke(playerlogger)
async def adduser(ctx, *args):
    """Adds user to the database"""
    view = Confirm()
    await ctx.send('Confirmation to add {} to the database'.format(args[0]), view=view)
    # Wait for the View to stop listening for input...
    await view.wait()
    if view.value is None:
        await ctx.send('Timed out...')
    elif view.value:
        if (await DB.adduser(ctx.author.id, ctx.author.name)):
            await ctx.send('Confirmed, adding {} to the database...'.format(args[0]))
        else:
            await ctx.send("{} already exists in the database.".format(args[0]))
    else:
        await ctx.send('Cancelled...{} was not added.'.format(args[0]))


# @bot.command()
# @commands.is_owner()
# async def reload(ctx, extension):
#     await bot.reload_extension(f"cogs.{extension}")
#     embed = discord.Embed(title='Reloaded', description=f'{extension} successfully reloaded!', color=0xff00c8)
#     await ctx.send(embed=embed)


@bot.command()
async def setbirthday(ctx, month, day, year):
    birthday = "{0}-{1}-{2}".format(month, day, year)
    await ctx.send(birthday)
    DB.setBirthday(ctx.author.id, birthday)


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
