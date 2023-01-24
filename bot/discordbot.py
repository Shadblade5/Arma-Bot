import discord
from discord.ext import commands, tasks
from bot import views, config, database
import pytz
import sys
import os
from wakeonlan import send_magic_packet

description = '''Here are the following commands available.'''

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

LAN_WAKEUP_CODE = 'E0-D5-5E-28-75-DE'

NEW_COC_CHANNEL_ID = 1053239585838215229
BOT_LOG_CHANNEL_ID = 1066975056024064032

PERM_ROLE_OFFICER = 'Officer'
PERM_ROLE_ADMINNCO = 'Admin-NCO'
PERM_ROLE_SENIORNCO = 'Senior-NCO'

BOT_ACTIVITY_TYPE = discord.ActivityType.watching
BOT_ACTIVITY_TEXT = 'the server burn'
BOT_ACTIVITY = discord.Activity(type=BOT_ACTIVITY_TYPE, name=BOT_ACTIVITY_TEXT)

BOT_TIMEZONE = pytz.timezone('US/Eastern')

DOCKER_HOSTNAME = 'host.docker.internal'

# To make this a production environment, simply run the bot with the environment variable
# `BOT_DEBUG_ENVIRONMENT=0`
BOT_DEBUG_ENVIRONMENT = os.environ.get('BOT_DEBUG_ENVIRONMENT', '1') == '1'

ADDUSER_MAX_ATTEMPTS_PER_PERIOD = 1
ADDUSER_COOLDOWN_PERIOD = 60

DISCORD_BUCKETTYPE_GUILD = commands.BucketType.guild


if BOT_DEBUG_ENVIRONMENT:
    configuration = config.LoadConfig(config.DEBUG_LOAD_CONFIG_PATH)
else:
    configuration = config.ConfigFromEnv()


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
    await bot.change_presence(activity=BOT_ACTIVITY)
    check_for_restart.start()


async def playerlogger(ctx):
    channel = bot.get_channel(BOT_LOG_CHANNEL_ID)
    timestamp = ctx.message.created_at.astimezone(BOT_TIMEZONE)
    em = discord.Embed()
    em.set_thumbnail(url=ctx.author.display_avatar.url)
    em.thumbnail.width = 20
    em.thumbnail.height = 20
    em.title = f'{ctx.author.name}#{ctx.author.discriminator}'
    em.add_field(name='Command Used', value=ctx.command)
    Args = ctx.message.content.split(
        bot.command_prefix + ctx.command.name + ' ')
    if (len(Args) > 1):
        em.add_field(name='Arguments', value=Args[1], inline=False)
    em.set_footer(text='{}'.format(
        timestamp.strftime('%Y-%m-%d at %I:%M:%S %p %Z')))
    em.colour = discord.Colour.blue()
    await channel.send(embed=em)


@bot.event
async def on_member_join(ctx):
    await DB.adduser(ctx.id, ctx.name)


@bot.command(name='getusers')
async def get_users(ctx):
    await ctx.send(await DB.getUsers())


@bot.command(name='getuserinfo')
async def get_user_info(ctx):
    message = await ctx.send('Getting user info...')
    userinfo = await DB.getUserInfo(ctx.author.id)
    await message.edit(
        content=f'Name: {userinfo[1]}\nDiscordID: {userinfo[0]}\nGrade: {userinfo[2]}\nJoinDate: {userinfo[4]}\nBirthday: {userinfo[5]}'
    )


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
@commands.has_any_role(PERM_ROLE_OFFICER, PERM_ROLE_ADMINNCO)
async def startserver(ctx):
    await ctx.send('Attempting to start server, please wait...')
    send_magic_packet(LAN_WAKEUP_CODE)


def RestartBot(filehandle):
    filehandle.seek(0)  # Return to top of file
    filehandle.write('0')
    filehandle.close()
    print('Restarting....')
    # os.execv(sys.executable, ['python'] + sys.argv)
    sys.exit()  # If running in a docker container with restart_always, this should automatically restart the bot


@tasks.loop(minutes=1)
async def check_for_restart():
    with open('restartflag.txt', 'r+') as f:
        if (f.readline(1) == '1'):
            RestartBot(f)


@bot.command()
@commands.has_any_role(PERM_ROLE_OFFICER)
@commands.after_invoke(playerlogger)
async def rankup(ctx, member: discord.Member):
    # myguild = ctx.guild
    # guildroles = await myguild.fetch_roles()
    memberRoles = member.roles
    oldGrade = None
    # oldGradeID = None
    for role in memberRoles:
        if ('Unit Grade' in role.name):
            oldRole = role
            oldGrade = role.name

            # Todo(Cabal): Make this cleaner
            oldgradeNumber = [int(x) for x in oldGrade.split() if x.isdigit()][0]
            # oldGradeID = role.id
    if oldGrade is None:
        await ctx.send(f'Error! {member.name} doesn\'t have a unit grade')
    else:
        # oldRole = discord.utils.get(ctx.guild.roles, name="Unit Grade {}".format(oldgradeNumber))
        newRole = discord.utils.get(
            ctx.guild.roles, name=f'Unit Grade {oldgradeNumber + 1}')

        await member.add_roles(newRole, reason='Rankup')
        await member.remove_roles(oldRole, reason='Rankup')

        await ctx.send(f'{member.name} ranked up to Unit Grade {oldgradeNumber + 1}')


@bot.command()
@commands.has_any_role(
    PERM_ROLE_OFFICER,
    PERM_ROLE_ADMINNCO,
    PERM_ROLE_SENIORNCO
)
@commands.cooldown(ADDUSER_MAX_ATTEMPTS_PER_PERIOD, ADDUSER_COOLDOWN_PERIOD, DISCORD_BUCKETTYPE_GUILD)
@commands.max_concurrency(ADDUSER_MAX_ATTEMPTS_PER_PERIOD, per=DISCORD_BUCKETTYPE_GUILD, wait=True)
@commands.after_invoke(playerlogger)
async def adduser(ctx, *args):
    """Adds user to the database"""
    view = views.ConfirmView()
    await ctx.send(f'Confirmation to add {args[0]} to the database', view=view)
    # Wait for the View to stop listening for input...
    await view.wait()
    if view.value is None:
        await ctx.send('Timed out...')
    elif view.value:
        if (await DB.adduser(ctx.author.id, ctx.author.name)):
            await ctx.send(f'Confirmed, adding {args[0]} to the database...')
        else:
            await ctx.send(f'{args[0]} already exists in the database.')
    else:
        await ctx.send(f'Cancelled...{args[0]} was not added.')


@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    await bot.reload_extension(f'cogs.{extension}')
    embed = discord.Embed(
        title='Reloaded', description=f'{extension} successfully reloaded!', color=0xff00c8)
    await ctx.send(embed=embed)


@bot.command()
async def setbirthday(ctx, month, day, year):
    birthday = f'{month}-{day}-{year}'
    await ctx.send(birthday)
    DB.setBirthday(ctx.author.id, birthday)


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
