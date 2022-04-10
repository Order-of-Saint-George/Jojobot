import discord
import time
import re
import random
import json
from discord.ext import commands
from discord.message import PartialMessage
from discord_slash import SlashCommand, SlashContext, utils

with open('settings.json') as f:
    settings = json.load(f)

TOKEN = settings["Token"]
mainChannel = settings["generalChannel"]

if(TOKEN == "TOKEN" or mainChannel == 0):
    print("Token and/or main channel need to be entered in settings.json file")
    time.sleep(5)
    exit()


#client = discord.Client()
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        print('Greeting...')
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
        return

    # whitespace splitting: !say channelID message
    # if (message.channel.id == '<CHANNEL ID>') & message.content.startswith('!say'):
    ##          data = message.content.split()
    ##          msg = ''
    # for temp in data[2:]:
    ##                  msg = msg + temp + ' '
    ##          print ('Echoing message: channel {0}, message {1}'.format(data[1], msg))
    # await client.send_message(client.get_channel(data[1]), msg)
    # return

    if message.content.startswith('!roll'):
        # need to split out verbose mode
        data = (message.content + ' PlaceHoldText').split()
        msg = data[1].lower()
        print('Random roll on channel {0}, message {1}'.format(
            message.channel.id, msg))

        # Check for proper format
        DieResult = 'Please use the format XdY+Z, XdY-Z, or XdY_T (for White Wolf-esque threshold dice). No spaces. Don\'t use 1000+ dice, 1000000+ sides, or a 10+ digit modifier.'
        MainPattern = re.compile(
            "^([0-9]{1,4})[dD]([0-9]{1,7})([+-_])([0-9]{1,10})")
        ShortPattern = re.compile("^([0-9]{1,4})[dD]([0-9]{1,7})$")
        # Group 0: full match
        # Group 1: die count
        # Group 2: die size
        # Group 3: operator character
        # Group 4: modifier or threshold
        matchFormat = re.search(MainPattern, msg)
        matchFormatShort = re.search(ShortPattern, msg)

        if matchFormat:
            DieNum = int(matchFormat.group(1))
            DieSize = int(matchFormat.group(2))
            DieOper = str(matchFormat.group(3))
            DieModThresh = int(matchFormat.group(4))

            DieResult = 'Result: '
            ListRolls = []
            NumDiceLeft = DieNum

            while NumDiceLeft > 0:
                ListRolls.append(random.randint(1, DieSize))
                NumDiceLeft = NumDiceLeft - 1

            if DieOper == '+':
                TotalRoll = 0
                for f in ListRolls:
                    TotalRoll = TotalRoll + f
                TotalRoll = TotalRoll + DieModThresh
                DieResult = DieResult + str(TotalRoll)
            elif DieOper == '-':
                TotalRoll = 0
                for f in ListRolls:
                    TotalRoll = TotalRoll + f
                TotalRoll = TotalRoll - DieModThresh
                DieResult = DieResult + str(TotalRoll)
            elif DieOper == '_':
                TotalRoll = 0
                for f in ListRolls:
                    myint = 0 if (f-DieModThresh) < 0 else 1
                    TotalRoll = TotalRoll + myint  # negatives to 0, zero or positive to 1
                TotalRoll = int(TotalRoll)
                DieResult = DieResult + str(TotalRoll) + ' successes'
            else:
                DieResult = 'Bad operator.'
                print('bad operator bug')
                return
            DieResult = DieResult + '; dice results: '

            FullDieList = ''
            for f in ListRolls:
                FullDieList = FullDieList + str(f) + ', '
            # remove last comma-space chars
            FullDieList = FullDieList[0:(len(FullDieList)-2)]

            DieResult = DieResult + FullDieList
        elif matchFormatShort:
            DieNum = int(matchFormatShort.group(1))
            DieSize = int(matchFormatShort.group(2))

            DieResult = 'Result: '
            ListRolls = []
            NumDiceLeft = DieNum

            while NumDiceLeft > 0:
                ListRolls.append(random.randint(1, DieSize))
                NumDiceLeft = NumDiceLeft - 1

            TotalRoll = 0
            for f in ListRolls:
                TotalRoll = TotalRoll + f

            DieResult = DieResult + str(TotalRoll)
            DieResult = DieResult + '; dice results: '

            FullDieList = ''
            for f in ListRolls:
                FullDieList = FullDieList + str(f) + ', '
            # remove last comma-space chars
            FullDieList = FullDieList[0:(len(FullDieList)-2)]
            DieResult = DieResult + FullDieList
        else:
            await message.channel.send('{0}'.format(DieResult), delete_after=45.0)
            return
        await message.channel.send('{0}'.format(DieResult))
        return

    if (str.upper(message.content).find("METAL GEAR") != -1):
        msg = 'Metal... Gear?'
        print('Metal Gear detected in channel {0}.'.format(message.channel.id))
        await message.channel.send(msg)
        return

    if (str.upper(message.content).find("WATCH JOJO") != -1):
        msg = 'You should watch Jojo!'
        print('It seems there is the work of an enemy stand in channel {0}.'.format(
            message.channel.id))
        await message.channel.send(msg)
        return

    if (str.lower(message.content).find("media.discordapp.net") != -1):
        await message.reply(message.author.mention + " " + message.content.replace("media.discordapp.net", "cdn.discordapp.com"))

    print('message from channel {0} had no action.'.format(message.channel.id))
    return


@client.event
async def on_member_join(member):
    print('New member on server {0}'.format(member.guild.id))
    if (member != client.user) & (member.guild.id == mainChannel):
        msg = 'Hello {0.mention}, welcome to the Order of St. George! We hope you enjoy your flight!'.format(
            member)
        await client.get_channel(mainChannel).send(msg)
        return


@client.event
async def on_ready():
    print('Logged in as: '+client.user.name)
    print('Bot ID: '+str(client.user.id))
    for server in client.guilds:
        print("Connected to server: {}".format(server))
    print('------')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Jojo"))

options = [
    {
        "name": "dice",
        "description": "Please use the format XdY+Z, XdY-Z, or XdY_T (for White Wolf-esque threshold dice)",
        "required": True,
                "type": 3
    },
    {
        "name": "name",
        "description": "Who rolled the dice? Can be used to fill a character or NPC name",
        "required": False,
                "type": 3
    }
]


@slash.slash(name="roll", description="roll some dice, be careful of sirens though, they're allergic.", options=options)
async def roll(ctx: SlashContext, dice: str, name=None):
    roll = dice.replace(' ', '')
    totalRolled = []
    succRolled = 0
    sumTotal = 0
    validRoll = bool(re.match(
        '^([\+\-]?[0-9]+([dD][0-9]+(\_[0-9]+)?)?([\+\-][0-9]+([dD][0-9]+(\_[0-9]+)?)?)*)$', roll))
    x = roll.replace("+", ' +').replace('-', ' -').replace('D', 'd').split()
    if validRoll:
        for k in x:
            k.strip()
            if('_' in k):
                sub = k.split("d")
                thresh = int(sub[-1].split('_')[-1])
                for _ in range(int(sub[0].strip())):
                    numRoll = random.randint(
                        1, int(sub[-1].split('_')[0].strip()))
                    totalRolled.append(numRoll)
                    succRolled = succRolled if (
                        numRoll-thresh) < 0 else succRolled + 1
            elif('d' in k):
                sub = k.split("d")
                sign = 1
                if int(sub[0].strip()) < 0:
                    sign = -1
                for _ in range(sign*int(sub[0].strip())):
                    numRoll = sign * random.randint(1, int(sub[-1].strip()))
                    totalRolled.append(numRoll)
                    sumTotal += numRoll

            else:
                totalRolled.append(int(k.strip()))
                sumTotal += int(k.strip())

        await ctx.send("{} rolled <{}> and got: {!s}{!s} {!s}".format(
            name if name else ctx.author.mention, roll.replace('_', ' with a threshold of ').replace('+', ' + ').replace('-', ' - '), sumTotal if sumTotal else '', ' <{!s} successes>'.format(succRolled) if '_' in roll else '', totalRolled))
    else:
        await ctx.send('Bad Formatting', hidden=True)


if __name__ == '__main__':
    client.run(TOKEN)

# while True:
#        try:
#                client.loop.run_until_complete(client.start(TOKEN))
#
#        except KeyboardInterrupt:
#                client.loop.run_until_complete(client.logout())
#                # cancel all tasks lingering
#                raise
#                #exit
#        except BaseException:
#                print('Retrying in 30 seconds...')
#                time.sleep(30)
