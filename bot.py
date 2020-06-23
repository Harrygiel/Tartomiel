from datetime import datetime, timedelta
import discord
import botlib

remaTimer = datetime.now()
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    global remaTimer

    if message.author == client.user:
        return

    if message.content.lower().startswith('bonjour'):
        await message.channel.send(botlib.func_bonjour(message, client)) 

client.run('NzI1MDAyNTk3NTA0OTA5NDY1.XvIZxA.J6vhlvNaogttVqxYa2xpo9BsRCQ')