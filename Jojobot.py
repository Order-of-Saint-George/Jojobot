import discord,asyncio
import time
import re
import random
import math
import json

with open('settings.json') as f:
	settings = json.load(f)

TOKEN = settings["Token"]
mainChannel = settings["generalChannel"]

if(TOKEN == "TOKEN" or mainChannel == 0):
        print ("Token and/or main channel need to be entered in settings.json file")
        time.sleep(5)
        exit()

client = discord.Client()

@client.event
async def on_message(message):
        # we do not want the bot to reply to itself
        if message.author == client.user:
                return
        
        if message.content.startswith('!hello'):
                print ('Greeting...')
                msg = 'Hello {0.author.mention}'.format(message)
                await message.channel.send(msg)
                return
                
##      whitespace splitting: !say channelID message
##      if (message.channel.id == '<CHANNEL ID>') & message.content.startswith('!say'):
##                data = message.content.split()
##                msg = ''
##                for temp in data[2:]:
##                        msg = msg + temp + ' '
##                print ('Echoing message: channel {0}, message {1}'.format(data[1], msg))
##                await client.send_message(client.get_channel(data[1]), msg)
##                return

        if message.content.startswith('!roll'):
                #need to split out verbose mode
                data = (message.content + ' PlaceHoldText').split()
                msg = data[1].lower()
                print ('Random roll on channel {0}, message {1}'.format(message.channel.id, msg))
                
                #Check for proper format
                DieResult = 'Please use the format XdY+Z, XdY-Z, or XdY_T (for White Wolf-esque threshold dice). No spaces. Don\'t use 1000+ dice, 1000000+ sides, or a 10+ digit modifier.'
                MainPattern = re.compile("^([0-9]{1,4})[dD]([0-9]{1,7})([+-_])([0-9]{1,10})")
                ShortPattern = re.compile("^([0-9]{1,4})[dD]([0-9]{1,7})$")
                #Group 0: full match
                #Group 1: die count
                #Group 2: die size
                #Group 3: operator character
                #Group 4: modifier or threshold
                matchFormat = re.search(MainPattern,msg)
                matchFormatShort = re.search(ShortPattern,msg)
                
                if matchFormat:
                        DieNum = int(matchFormat.group(1))
                        DieSize = int(matchFormat.group(2))
                        DieOper = str(matchFormat.group(3))
                        DieModThresh = int(matchFormat.group(4))
                        
                        DieResult = 'Result: '
                        ListRolls = []
                        NumDiceLeft = DieNum

                        while NumDiceLeft > 0:
                                ListRolls.append(random.randint(1,DieSize))
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
                                        TotalRoll = TotalRoll + myint # negatives to 0, zero or positive to 1
                                TotalRoll = int(TotalRoll)
                                DieResult = DieResult + str(TotalRoll) + ' successes'
                        else:
                                DieResult = 'Bad operator.'
                                print ('bad operator bug')
                                return
                        DieResult = DieResult + '; dice results: '
                        
                        FullDieList = ''
                        for f in ListRolls:
                                FullDieList = FullDieList + str(f) + ', '
                        FullDieList = FullDieList[0:(len(FullDieList)-2)] #remove last comma-space chars
                                
                        DieResult = DieResult + FullDieList
                elif matchFormatShort:
                        DieNum = int(matchFormatShort.group(1))
                        DieSize = int(matchFormatShort.group(2))

                        DieResult = 'Result: '
                        ListRolls = []
                        NumDiceLeft = DieNum

                        while NumDiceLeft > 0:
                                ListRolls.append(random.randint(1,DieSize))
                                NumDiceLeft = NumDiceLeft - 1
                        
                        TotalRoll = 0
                        for f in ListRolls:
                                TotalRoll = TotalRoll + f
                                
                        DieResult = DieResult + str(TotalRoll)
                        DieResult = DieResult + '; dice results: '

                        
                        FullDieList = ''
                        for f in ListRolls:
                                FullDieList = FullDieList + str(f) + ', '
                        FullDieList = FullDieList[0:(len(FullDieList)-2)] #remove last comma-space chars
                        DieResult = DieResult + FullDieList
                else:
                        await message.channel.send('{0}'.format(DieResult), delete_after = 45.0)
                        return
                await message.channel.send('{0}'.format(DieResult))
                return

        if (str.upper(message.content).find("METAL GEAR") != -1):
                msg = 'Metal... Gear?'
                print ('Metal Gear detected in channel {0}.'.format(message.channel.id))
                await message.channel.send(msg)
                return
        
        if (str.upper(message.content).find("WATCH JOJO") != -1):
                msg = 'You should watch Jojo!'
                print ('It seems there is the work of an enemy stand in channel {0}.'.format(message.channel.id))
                await message.channel.send(msg)
                return

        print ('message from channel {0} had no action.'.format(message.channel.id))
        return
        
@client.event
async def on_member_join(member):
        print ('New member on server {0}'.format(member.guild.id))
        if (member != client.user) & (member.guild.id == mainChannel):
                msg = 'Hello {0.mention}, welcome to the Order of St. George! We hope you enjoy your flight!'.format(member)
                await client.get_channel(mainChannel).send(msg)
                return

@client.event
async def on_ready():
        print('Logged in as: '+client.user.name)
        print('Bot ID: '+str(client.user.id))
        for server in client.guilds:
                print ("Connected to server: {}".format(server))
        print('------')
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Jojo"))


while True:
        try:
                client.loop.run_until_complete(client.start(TOKEN))
                
        except KeyboardInterrupt:
                client.loop.run_until_complete(client.logout())
                # cancel all tasks lingering
                raise
                #exit
        except BaseException:
                print('Retrying in 30 seconds...')
                time.sleep(30)
