import discord
import botlib

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('bonjour'):
        await message.channel.send(botlib.func_bonjour(message, client)) 

    if message.content.lower().startswith('!quest') or message.content.lower().startswith('!quete'):
        await botlib.Quest_Manager(message, client)
        #string = botlib.Generate_Table(message, client)
        #print(string)
        #await message.channel.send(string) 

client.run('NzI1MDAyNTk3NTA0OTA5NDY1.XvIZxA.J6vhlvNaogttVqxYa2xpo9BsRCQ')