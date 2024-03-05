import discord
import datetime
import scumftp
import killparse
import chatparse
import loginparse
from discord.ext import commands, tasks
import configparser
import datetime as dt
from datetime import timedelta
# Gansta-Girs OpenSource
intents = discord.Intents.all()

client = commands.Bot(command_prefix='!',intents=intents)
config = configparser.ConfigParser()
config.read('config.ini')
last_chat_dt = 0
last_kill_dt = 0
last_login_dt = 0
chat_channel = int(config['DISCORD']['chat_channel'])
kill_channel = int(config['DISCORD']['kill_channel'])
login_channel = int(config['DISCORD']['login_channel'])
#login_channel = 0
TOKEN = config['DISCORD']['token']
DELAY = config['DISCORD']['delay']
DELAY = int(DELAY)


@client.event
async def on_ready():
    global last_chat_dt, last_kill_dt, last_login_dt
    last_chat_dt =  dt.datetime.now() - timedelta(hours=3)
    last_kill_dt =  dt.datetime.now() - timedelta(hours=3)
    last_login_dt =  dt.datetime.now() - timedelta(hours=3)
    check_files.start()


async def post_chat_events(chat_events):
    global chat_channel
    channel = chat_channel
    for chat_event in chat_events:
        out = "```fix\n" + str(chat_event['date'].strftime("%Y-%m-%d %H:%M")) + " from " + chat_event['user'] + "```\n" + chat_event['message']
        await client.get_channel(channel).send(out)


async def post_kill_events(kill_events):
    global kill_channel
    channel = kill_channel
    for kill_event in kill_events:
        message = discord.Embed(
            title="Kill",
            color=discord.Color.red()
        )
        message.add_field(name="Killer", value=kill_event['killer'], inline=True)
        message.add_field(name="Location", value=kill_event['killerLoc'], inline=True)
        message.add_field(name="Victim", value=kill_event['victim'], inline=False)
        message.add_field(name="VictimLocation", value=kill_event['victimLoc'], inline=True)
        message.add_field(name="Weapon", value=kill_event['weapon'], inline=False)
        image_url = 'http://www.tvanderbruggen.com/scum/kill_' + kill_event['victimLoc'] + ".png"
        message.set_image(url=image_url)
        await client.get_channel(channel).send(embed=message)


async def post_login_events(login_events):
    global login_channel
    channel = login_channel
    for login in login_events:
        await client.get_channel(channel).send(login['user'] + " logged in")


@tasks.loop(seconds=DELAY)
async def check_files():
    print("Checking for new files at ", dt.datetime.now())
#    await client.get_channel(login_channel).send("test logged in")
    global config, last_login_dt, last_chat_dt, last_kill_dt
    new_files = scumftp.check_files(config['FTP'], last_chat_dt, last_kill_dt, last_login_dt)
    if len(new_files) > 0:
        for file in new_files:
            print("Reading file:", file)
            if file.startswith("chat_"):
                chat_events = chatparse.parse_chat(file, last_chat_dt)
                if len(chat_events) > 0:
                    last_chat_dt = chat_events[len(chat_events)-1]['date']
                    await post_chat_events(chat_events)
            elif file.startswith("kill_"):
                kill_events = killparse.parse_kill(file, last_kill_dt)
                if len(kill_events) > 0:
                    last_kill_dt = kill_events[len(kill_events)-1]['date']
                    await post_kill_events(kill_events)
            elif file.startswith("login_"):
                #with open(file, "r") as rfile:
                #    content = rfile.read()
                #    print(f"Content of {file}:\n{content}")
                login_events = loginparse.parse_login(file, last_login_dt)
                print("Events",login_events)
                if len(login_events) > 0:
                    last_login_dt = login_events[len(login_events)-1]['date']
                    await post_login_events(login_events)
    scumftp.delete_files(new_files)


client.run(TOKEN)
