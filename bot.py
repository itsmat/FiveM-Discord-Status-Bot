### Lib ###
import nextcord
import datetime
from nextcord.ext import commands, tasks
from requests import get

### Config ###
BOT_TOKEN = '' #Required

SERVER_IP = ''   #Required
SERVER_PORT = ''       #Required
CONNECT = ''         #Recommended
SERVER_NAME = ''       #Recommended
STATUS_IMAGE = ''           #Optional

SECONDS = 15                           #Required
CHANNEL_ID = 1       #Required
MESSAGE_ID = 1       #Required

ERRORCOLOR = 0xff0000
DONECOLOR = 0x00ff2e

### Setup ###
class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

bot = Bot()

### Bot ###
@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.playing, name='''💖 By Mat#3616 - github.com/itsmat'''))
    print('\nBot Online - github.com/itsmat')
    if SERVER_IP == '':
        print('SERVER_IP MISSING')
    if SERVER_PORT == '':
        print('SERVER_PORT MISSING')
    if CONNECT == '':
        print('CONNECT MISSING')
    if CHANNEL_ID == 1:
        print('CHANNEL_ID MISSING')
    if MESSAGE_ID == 1:
        print('MESSAGE_ID MISSING')


@bot.slash_command(
    name="status",
    description="Server Status",
)
async def status(interaction: nextcord.Interaction):
    try:
        if SERVER_IP and SERVER_PORT != '':
            filedynamic = get(f'http://{SERVER_IP}:{SERVER_PORT}/dynamic.json', timeout=10)
            filedynamic = filedynamic.json()
            playersonline = str(filedynamic["clients"])
            playersmassimi = str(filedynamic["sv_maxclients"])
            embed=nextcord.Embed(title="", description=f"**Connect:** `connect {CONNECT}`\n**Players:** {playersonline}/{playersmassimi}", color=DONECOLOR)
            embed.set_author(name=F"{SERVER_NAME} Status", url="https://github.com/itsmat", icon_url=STATUS_IMAGE)
            if STATUS_IMAGE != '':
                embed.set_image(url=STATUS_IMAGE)
            else:
                pass
            embed.set_footer(text="""💖 By Mat#3616 - github.com/itsmat""")
            await interaction.send(embed=embed)
        else:
            if SERVER_IP == '':
                print('SERVER_IP MISSING')
            if SERVER_PORT == '':
                print('SERVER_PORT MISSING')
            if CONNECT == '':
                print('CONNECT MISSING')
            embed=nextcord.Embed(title="Error", description=f"Missing data", color=ERRORCOLOR)
            embed.set_footer(text="""💖 By Mat#3616 - github.com/itsmat""")
            await interaction.send(embed=embed)
    except Exception as errore:
        print(f'[/Status Error] {errore}')



@bot.slash_command(
    name="createstatus",
    description="Create Status Message",
)
async def createstatus(interaction: nextcord.Interaction):
    embed=nextcord.Embed(title="Ok", description=f"Channel ID: `{interaction.channel.id}`", color=DONECOLOR)
    embed.set_footer(text="""💖 By Mat#3616 - github.com/itsmat""")
    await interaction.send(embed=embed)




@tasks.loop(seconds = SECONDS)
async def autostatus():
    print("[AutoStatus] Searching for info...")
    try:
        await bot.wait_until_ready()
        filedynamic = get(f'http://{SERVER_IP}:{SERVER_PORT}/dynamic.json', timeout=10)
        fileplayers = get(f'http://{SERVER_IP}:{SERVER_PORT}/players.json', timeout=10)
        canale = bot.get_channel(CHANNEL_ID)
        messaggio = await canale.fetch_message(MESSAGE_ID)
        if filedynamic.status_code == 200 or fileplayers.status_code == 200 :
            filedynamic = filedynamic.json()
            fileplayers = fileplayers.json()
            embed=nextcord.Embed(color=DONECOLOR, timestamp = datetime.datetime.utcnow())
            embed.add_field(name="IP Fivem", value=f"```connect {CONNECT}```", inline=False)
            embed.add_field(name="Players", value='```ini\n[' + str(filedynamic["clients"]) + "/" + str(filedynamic["sv_maxclients"]) + ']\n```', inline=True)
            embed.add_field(name="Status", value=f"""```fix
Online
```""", inline=True)
            embed.set_author(name=SERVER_NAME, url="https://github.com/itsmat", icon_url=STATUS_IMAGE)
            embed.set_thumbnail(url=STATUS_IMAGE)
            embed.set_footer(text='''💖 By Mat#3616 - github.com/itsmat''', icon_url=STATUS_IMAGE)

            try:
                await messaggio.edit(embed=embed)
            except Exception:
                print("[AutoStatus] Message not editable, reset it")
        else:
            embed=nextcord.Embed(color=0x5a03fc, timestamp = datetime.datetime.utcnow())
            embed.add_field(name="IP Fivem", value=f"```connect {CONNECT}```", inline=False)
            embed.add_field(name="Players", value='```ini\n[Server Offline]\n```', inline=True)
            embed.add_field(name="Status", value=f"""```fix
Offline
```""", inline=True)
            embed.set_author(name=SERVER_NAME, url="https://github.com/itsmat", icon_url=STATUS_IMAGE)
            embed.set_thumbnail(url=STATUS_IMAGE)
            embed.set_footer(text='''💖 By Mat#3616 - github.com/itsmat''', icon_url=STATUS_IMAGE)
            try:
                await messaggio.edit(embed=embed)
            except Exception:
                print("[AutoStatus] Message not editable, reset it")
    except Exception as errore:
        print(f'[AutoStatus Error] {errore}')
        



autostatus.start()
bot.run(BOT_TOKEN)