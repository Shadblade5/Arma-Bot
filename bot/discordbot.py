import discord
from discord.ext import commands
import config
import database
import pytz
import os
from wakeonlan import send_magic_packet
import views

description = '''Here are the following commands available.'''

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

LAN_WAKEUP_CODE = 'E0-D5-5E-28-75-DE'

NEW_COC_CHANNEL_ID = 1053239585838215229
BOT_LOG_CHANNEL_ID = 941879875059449946

Director = 1066598944701960192
CertSepRole = 978788249726226463
RankSepRole = 1069114415842074684
CampSepRole = 1066967939024175154
DLCSepRole = 978786976050339941
NeedBCCRole = 992820081602088981


RoleSeperators = {CertSepRole, RankSepRole, CampSepRole, DLCSepRole}

# BOT_ACTIVITY_TYPE = discord.ActivityType.watching
# BOT_ACTIVITY_TEXT = 'the server burn'
# BOT_ACTIVITY = discord.Activity(type=BOT_ACTIVITY_TYPE, name=BOT_ACTIVITY_TEXT)

BOT_TIMEZONE = pytz.timezone('US/Eastern')

DOCKER_HOSTNAME = 'host.docker.internal'

# To make this a production environment, simply run the bot with the environment variable
# `BOT_DEBUG_ENVIRONMENT=0`
BOT_DEBUG_ENVIRONMENT = os.environ.get('BOT_DEBUG_ENVIRONMENT', '1') == '1'

ADDUSER_MAX_ATTEMPTS_PER_PERIOD = 1
ADDUSER_COOLDOWN_PERIOD = 60

DISCORD_BUCKETTYPE_GUILD = commands.BucketType.guild


if BOT_DEBUG_ENVIRONMENT:
    configuration = config.load_config(config.DEBUG_LOAD_CONFIG_PATH)
else:
    configuration = config.create_config_from_environment()

bot = commands.Bot(command_prefix=configuration.prefix,
                   description=description, intents=intents)
DB = database.Database(configuration.db_host, configuration.db_username,
                       configuration.db_password, database.DATABASE_NAME)


@bot.event
async def on_ready():
    print('Logged in as')
    output = bot.user.name + ' ID:' + str(bot.user.id)
    print(output)
    print('-' * len(output))
    # await bot.change_presence(activity=BOT_ACTIVITY)


async def playerlogger(ctx):
    channel = bot.get_channel(BOT_LOG_CHANNEL_ID)
    timestamp = ctx.message.created_at.astimezone(BOT_TIMEZONE)
    em = discord.Embed()
    em.set_thumbnail(url=ctx.author.display_avatar.url)
    em.thumbnail.width = 20
    em.thumbnail.height = 20
    em.title = f'{ctx.author.name}#{ctx.author.discriminator}'
    em.add_field(name='Command Used', value=ctx.command)
    args = ctx.message.content.split(
        bot.command_prefix + ctx.command.name + ' ')
    if (len(args) > 1):
        em.add_field(name='Arguments', value=args[1], inline=False)
    em.set_footer(text=f'{timestamp.strftime("%Y-%m-%d at %I:%M:%S %p %Z")}')
    em.colour = discord.Colour.blue()
    await channel.send(embed=em)


@bot.event
async def on_member_join(ctx):
    await ctx.member.roles.add(992820081602088981)

    # await DB.adduser(ctx.id, ctx.name)

# @bot.command(name='getusers')
# async def get_users(ctx):
#     await ctx.send(await DB.getUsers())


# @bot.command(name='getuserinfo')
# async def get_user_info(ctx):
#     message = await ctx.send('Getting user info...')
#     userinfo = await DB.getUserInfo(ctx.author.id)
#     await message.edit(
#         content=f'Name: {userinfo[1]}\nDiscordID: {userinfo[0]}\nGrade: {userinfo[2]}\nJoinDate: {userinfo[4]}\nBirthday: {userinfo[5]}'
#     )


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

    def __init__(self, *args):
        self.Section = args[0]
        self.Subsection = args[1]
        self.Item = args[2]
        self.Title = args[3]
        self.Description = args[4]


@bot.command()
@commands.has_any_role(Director)
async def createcoc(ctx):
    channel = bot.get_channel(NEW_COC_CHANNEL_ID)  # new-code-of-conduct
    print('Getting COC DATA')
    # threads = []
    coc = await DB.getcoc()
    # sorted_coc = sorted(
    #     coc,
    #     key=lambda t: (t[0], t[1], t[2])
    # )
    for code in coc:
        # print('{}.{}.{} {}'.format(*code))

        current_code = COC(*code)
        # print(f'Current: {current_code.Section}.{current_code.Subsection}.{current_code.Item}')
        last_code = None

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
                    current_code.em.add_field(
                        name=current_code.Title, value=current_code.Description, inline=False)

        last_code = current_code


@bot.command()
@commands.has_any_role(Director)
async def startserver(ctx):
    await ctx.send('Attempting to start server, please wait...')
    send_magic_packet(LAN_WAKEUP_CODE)


@bot.command()
@commands.has_any_role(Director)
@commands.after_invoke(playerlogger)
async def rankup(ctx, member: discord.Member):
    # myguild = ctx.guild
    # guildroles = await myguild.fetch_roles()
    member_roles = member.roles
    old_grade = None
    # oldGradeID = None
    for role in member_roles:
        if ('Unit Grade' in role.name):
            old_role = role
            old_grade = role.name

            # Todo(Cabal): Make this cleaner
            old_grade_num = [int(x) for x in old_grade.split() if x.isdigit()][0]
            # oldGradeID = role.id
    if old_grade is None:
        await ctx.send(f'Error! {member.name} doesn\'t have a unit grade')
    else:
        # oldRole = discord.utils.get(ctx.guild.roles, name="Unit Grade {}".format(oldgradeNumber))
        new_role = discord.utils.get(
            ctx.guild.roles, name=f'Unit Grade {old_grade_num + 1}')

        await member.add_roles(new_role, reason='Rankup')
        await member.remove_roles(old_role, reason='Rankup')

        await ctx.send(f'{member.name} ranked up to Unit Grade {old_grade_num + 1}')

# Temp removed until database fix


@bot.command()
@commands.has_any_role('Trainer', 'Director')
# @commands.cooldown(ADDUSER_MAX_ATTEMPTS_PER_PERIOD, ADDUSER_COOLDOWN_PERIOD, DISCORD_BUCKETTYPE_GUILD)
@commands.max_concurrency(ADDUSER_MAX_ATTEMPTS_PER_PERIOD, per=DISCORD_BUCKETTYPE_GUILD, wait=True)
@commands.after_invoke(playerlogger)
async def adduser(ctx, member: discord.Member, bcc: bool):
    """Adds user to the database"""
    view = views.ConfirmView()
    await ctx.send_message(f'Confirmation to add {member.display_name} to the unit', view=view)
    # Wait for the View to stop listening for input...
    await view.wait()
    if view.value:
        await member.add_roles(discord.utils.get(ctx.guild.roles, name='Unit Grade 1'))
        await member.add_roles(discord.utils.get(ctx.guild.roles, name='Unit Member'))
        for role in RoleSeperators:
            await member.add_roles(discord.utils.get(ctx.guild.roles, id=role))
        if bcc:
            await member.add_roles(discord.utils.get(ctx.guild.roles, name='Need BCC Cert'))
        await member.remove_roles(discord.utils.get(ctx.guild.roles, name='On The Fence'))
        # if (await DB.adduser(ctx.author.id, ctx.author.name)):
        #     await ctx.send(f'Confirmed, adding {args[0]} to the database...')
        # else:
        #     await ctx.send(f'{args[0]} already exists in the database.')


# @bot.command()
# @commands.is_owner()
# async def reload(ctx, extension):
#     await bot.reload_extension(f'cogs.{extension}')
#     embed = discord.Embed(
#         title='Reloaded', description=f'{extension} successfully reloaded!', color=0xff00c8)
#     await ctx.send(embed=embed)


# @bot.command()
# async def setbirthday(ctx, month, day, year):
#     birthday = f'{month}-{day}-{year}'
#     await ctx.send(birthday)
    # DB.setBirthday(ctx.author.id, birthday)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.UserInputError):
        await ctx.send(error)
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title='Command on Cooldown', description=f'Try again in {error.retry_after:.2f}s.',
                           color=discord.Colour.red())
        await ctx.send(embed=em)


if __name__ == '__main__':
    bot.run(configuration.token)
