import discord
import asyncio
import botlib
import discordtoken

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('bonjour'):
        await asyncio.wait_for(message.channel.send(botlib.func_bonjour(message, client)), timeout=5.0)

    if message.content.lower().startswith('!quest') or message.content.lower().startswith('!quete'):
        await botlib.Quest_Command(message, client)
        #string = botlib.Generate_Table(message, client)
        #print(string)
        #await message.channel.send(string) 

loop = asyncio.get_event_loop()
loop.create_task(botlib.Quest_Manager())
loop.create_task(client.run(discordtoken.TOKEN))

loop.run_forever()

#asyncio.gather(botlib.Quest_Manager(), client.run(discordtoken.TOKEN))