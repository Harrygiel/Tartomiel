import os
import asyncio
import datetime
import discord
import string
import shlex
from dateutil.parser import parse
import __main__ as bot

DELIMITER = "+----------+-------+----------------------+----+--------------+\n"
TMPMESSAGETIMER = 10


def func_bonjour(message, client):
    if str(client.user.id) in message.content or "<@!" not in message.content:
        if is_same_user(message.author, "Harrygiel", "7564"):
            return 'Bonjour Créateur <@%s> !' % message.author.id
        else:
            return 'Bonjour <@%s> !' % message.author.id

async def Quest_Manager():
    print("Quest Manager Started")
    lastUpdate = datetime.date.today()-datetime.timedelta(days=-1)
    while 1:
        await asyncio.sleep(60)
        if(lastUpdate+datetime.timedelta(days=1) < datetime.date.today()):
            print("[" + datetime.date.today().strftime("%m/%d/%Y-%H:%M:%S") + "]" + "Last update is 1 day ago. AutoUpdating")
            lastUpdate = datetime.date.today()
            for file in os.listdir("tableList"):
                if file.endswith(".txt"):
                    await Auto_Update(int(file[:-4]), "tableList/" + file)

async def Quest_Command(message, client):
    global Gmessage
    Gmessage = message
    messageBody = message.content[7:]
    fileName = "tableList/" + str(message.channel.id) + ".txt"
    await asyncio.create_task(asyncio.wait_for(message.delete(delay=30), timeout=5.0))

    isAdmin = False
    if message.author.permissions_in(message.channel).manage_messages:
        isAdmin = True

    paramDict = Get_Parameters(messageBody)
    print(paramDict)
'''
    if messageBody.lower().startswith('+event') or messageBody.lower().startswith('+e'):
        if not isAdmin:
            return await asyncio.create_task(Send_Not_Admin_Message())
        await Call_Create_Event(message, fileName)
        await Call_Update(message.channel, fileName)

    elif messageBody.lower().startswith('-event') or messageBody.lower().startswith('-e'):
        if not isAdmin:
            return await asyncio.create_task(Send_Not_Admin_Message())
        await Call_Remove_Event(message, fileName)
        await Call_Update(message.channel, fileName)

    elif messageBody.lower().startswith('+play') or messageBody.lower().startswith('+p'):
        await Call_Create_Particip(message, fileName, message.author.id)
        await Call_Update(message.channel, fileName)

    elif messageBody.lower().startswith('-play') or messageBody.lower().startswith('-p'):
        await Call_Remove_Particip(message, fileName, message.author.id)
        await Call_Update(message.channel, fileName)

    elif messageBody.lower().startswith('generate'):
        if not isAdmin:
            return await asyncio.create_task(Send_Not_Admin_Message())
        await Call_Generate(message, fileName)

    elif messageBody.lower().startswith('update'):
        if not isAdmin:
            return await asyncio.create_task(Send_Not_Admin_Message())
        await Call_Update(message.channel, fileName)

    elif messageBody.lower().startswith('remove'):
        if not isAdmin:
            return await asyncio.create_task(Send_Not_Admin_Message())
        await Call_Remove(message, fileName)

    else:
        await message.channel.send("Commande non reconnu")
'''
################## CALL COMMAND STUFF

async def Call_Create_Event(message, fileName):
    messageBody = message.content[7:]
    questParameters = messageBody.split(" ")[1:]
    if len(questParameters) < 5:
        return await asyncio.create_task(Send_Tmp_Message(message.channel, "Ajouter un évènement demande plus de paramètre !", TMPMESSAGETIMER))

    if len(questParameters[0]) == 10:
        questParameters[0] = questParameters[0][:6] + questParameters[0][8:]
    questParameters[4] = only_numerics(questParameters[4])
    sessionDict = Get_Event_Dict(fileName)
    if questParameters[0]+questParameters[1]+questParameters[4] in sessionDict:
        return await asyncio.create_task(Send_Tmp_Message(message.channel, "L'évènement est déjà dans la table des quêtes !", TMPMESSAGETIMER))
        tmpMsg = await message.channel.send()
        await tmpMsg.delete(delay=10)
        return

    with open(fileName, "a") as fileP:
        fileP.write("\n" + questParameters[0] + "\\" + questParameters[1] + "\\" + questParameters[2] + "\\" + questParameters[3] + "\\" + questParameters[4] + "\\")
    return await asyncio.create_task(Send_Tmp_Message(message.channel, "Evènement Ajouté!", TMPMESSAGETIMER))

async def Call_Remove_Event(message, fileName):
    messageBody = message.content[7:]
    questParameters = messageBody.split(" ")[1:]
    if len(questParameters) < 3:
        return await asyncio.create_task(Send_Tmp_Message(message.channel, "Supprimer un évenement demande plus de paramètre !", TMPMESSAGETIMER))

    sessionDict = Get_Event_Dict(fileName)
    if len(questParameters[0]) == 10:
        questParameters[0] = questParameters[0][:6] + questParameters[0][8:]
    questParameters[2] = only_numerics(questParameters[2])
    if questParameters[0]+questParameters[1]+questParameters[2] in sessionDict:
        sessionDict.pop(questParameters[0]+questParameters[1]+questParameters[2])
        Set_Event_Dict(fileName, sessionDict)
        return await asyncio.create_task(Send_Tmp_Message(message.channel, "Evènement supprimé!", TMPMESSAGETIMER))
    else:
        return await asyncio.create_task(Send_Tmp_Message(message.channel, "L'évènement n'est pas dans la table des quêtes !", TMPMESSAGETIMER))

async def Call_Create_Particip(message, fileName, userID):
    messageBody = message.content[7:]
    questParameters = messageBody.split(" ")[1:]
    sessionDict = Get_Event_Dict(fileName)
    if len(questParameters[0]) == 10:
        questParameters[0] = questParameters[0][:6] + questParameters[0][8:]
    if len(questParameters) == 1:
        eventKeyArray = [k for k, v in sessionDict.items() if questParameters[0] in k]
        if len(eventKeyArray) == 0:
            return await asyncio.create_task(Send_Tmp_Message(message.channel, "L'évènement auquel vous voulez participer n'existe pas !", TMPMESSAGETIMER))
        elif len(eventKeyArray) > 1:
            return await asyncio.create_task(Send_Tmp_Message(message.channel, "Il y a plus d'un évènement ce jour ! veuillez préciser l'heure et le MJ dans la commande", TMPMESSAGETIMER))
        eventKey = eventKeyArray[0]
    elif len(questParameters) > 2:
        questParameters[2] = only_numerics(questParameters[2])
        eventKey = questParameters[0]+questParameters[1]+questParameters[2]
    else:
        return await asyncio.create_task(Send_Tmp_Message(message.channel, "Le nombre de paramètre n'est pas cohérant", TMPMESSAGETIMER))

    if not(eventKey in sessionDict):
        return await asyncio.create_task(Send_Tmp_Message(message.channel, "L'évènement auquel vous voulez participer n'existe pas !", TMPMESSAGETIMER))

    adminPerm = False
    if message.author.permissions_in(message.channel).manage_messages:
        adminPerm = True

    if adminPerm is not True and int(sessionDict[eventKey][3]) <= len(sessionDict[eventKey])-5:
        return await asyncio.create_task(Send_Tmp_Message(message.channel, "L'évènement est déjà complet !", TMPMESSAGETIMER))

    if len(questParameters) > 3:
        if adminPerm is not True:
            return await asyncio.create_task(Send_Tmp_Message(message.channel, "Vous n'avez pas les droits pour ajouter d'autre joueurs !", TMPMESSAGETIMER))

        for userName in questParameters[3:]:
            if userName != "":
                sessionDict[eventKey].append(only_numerics(userName))
        Set_Event_Dict(fileName, sessionDict)
        return await asyncio.create_task(Send_Tmp_Message(message.channel, "Les participants ont bien été ajouté, administrateur !", TMPMESSAGETIMER))

    if str(userID) in sessionDict[eventKey]:
        return await asyncio.create_task(Send_Tmp_Message(message.channel, "Vous participez déjà à cet évènement !", TMPMESSAGETIMER))

    sessionDict[eventKey].append(str(userID))
    Set_Event_Dict(fileName, sessionDict)
    return await asyncio.create_task(Send_Tmp_Message(message.channel, "Participation ajouté!", TMPMESSAGETIMER))

async def Call_Remove_Particip(message, fileName, userID):
    messageBody = message.content[7:]
    questParameters = messageBody.split(" ")[1:]
    sessionDict = Get_Event_Dict(fileName)
    if len(questParameters[0]) == 10:
        questParameters[0] = questParameters[0][:6] + questParameters[0][8:]
    if len(questParameters) == 1:
        eventKeyArray = [k for k, v in sessionDict.items() if questParameters[0] in k]
        if len(eventKeyArray) == 0:
            return await asyncio.create_task(Send_Tmp_Message(message.channel, "L'évènement auquel vous voulez participer n'existe pas !", TMPMESSAGETIMER))
        elif len(eventKeyArray) > 1:
            return await asyncio.create_task(Send_Tmp_Message(message.channel, "Il y a plus d'un évènement ce jour ! veuillez préciser l'heure et le MJ dans la commande", TMPMESSAGETIMER))
        eventKey = eventKeyArray[0]
    elif len(questParameters) > 2:
        questParameters[2] = only_numerics(questParameters[2])
        eventKey = questParameters[0]+questParameters[1]+questParameters[2]
    else:
        return await asyncio.create_task(Send_Tmp_Message(message.channel, "Le nombre de paramètre n'est pas cohérant", TMPMESSAGETIMER))

    if not(eventKey in sessionDict):
        return await asyncio.create_task(Send_Tmp_Message(message.channel, "L'évènement auquel vous voulez participer n'existe pas !", TMPMESSAGETIMER))

    adminPerm = False
    if message.author.permissions_in(message.channel).manage_messages:
        adminPerm = True

    if len(questParameters) > 3:
        if adminPerm is not True:
            return await asyncio.create_task(Send_Tmp_Message(message.channel, "Vous n'avez pas les droits pour supprimer d'autre joueurs !", TMPMESSAGETIMER))
        for userName in questParameters[3:]:
            sessionDict[eventKey].remove(only_numerics(userName))
        Set_Event_Dict(fileName, sessionDict)
        return await asyncio.create_task(Send_Tmp_Message(message.channel, "Les participants ont bien été retiré, administrateur !", TMPMESSAGETIMER))

    if str(userID) == sessionDict[eventKey][4]:
        return await asyncio.create_task(Send_Tmp_Message(message.channel, "Vous êtes le MJ !", TMPMESSAGETIMER))

    if not(str(userID) in sessionDict[eventKey]):
        return await asyncio.create_task(Send_Tmp_Message(message.channel, "Vous ne participez pas à cet évènement !", TMPMESSAGETIMER))
    sessionDict[eventKey].remove(str(userID))
    Set_Event_Dict(fileName, sessionDict)
    return await asyncio.create_task(Send_Tmp_Message(message.channel, "Participation supprimé!", TMPMESSAGETIMER))

async def Call_Generate(message, fileName):
    messageBody = message.content[7:]
    nbDay = 20
    noEmpty = False
    questParameters = messageBody.split(" ")[1:]
    for questParameter in questParameters:
        if questParameter.lower() == "-noempty" or questParameter.lower() == "-nonvide":
            noEmpty = True
            continue
        if questParameter.isnumeric():
            nbDay = int(questParameter)
            continue

    if os.path.exists(fileName):
        return await asyncio.create_task(Send_Tmp_Message(message.channel, "La table des quêtes a déjà été généré. Utilisez \"!quest remove\" pour la supprimer", TMPMESSAGETIMER))
    questTableArray = Generate_Table(fileName, nbDay, noEmpty)
    sentIdArray = []
    for questTableVal in questTableArray:
        sent = await message.channel.send(questTableVal)
        sentIdArray.append(str(sent.id))
    Generate_New_DB(fileName, sentIdArray, str(nbDay), str(noEmpty))

async def Auto_Update(channelID, fileName):
    channel = bot.client.get_channel(channelID)
    await Call_Update(channel, fileName)

async def Call_Update(channel, fileName):
    questMessageIDs = Get_Quest_Var(fileName, "messageID").split('\\')
    nbDay = int(Get_Quest_Var(fileName, "nbDay"))
    noEmpty = False
    if Get_Quest_Var(fileName, "noEmpty") == "True":
        noEmpty = True
    i = 0
    for questMessageID in questMessageIDs:
        questMsg = await channel.fetch_message(int(questMessageID))
        if (nbDay-7*i) > 7:
            await questMsg.edit(content=Generate_Table(fileName, 7, noEmpty, datetime.date.today()+datetime.timedelta(days=i*7))[0])
        else:
            await questMsg.edit(content=Generate_Table(fileName, (nbDay-7*i)%7, noEmpty, datetime.date.today()+datetime.timedelta(days=i*7))[0])
        i=i+1

async def Call_Remove(message, fileName):
    if not(os.path.exists(fileName)):
        tmpMsg = await message.channel.send("Aucune table des quêtes n'a été trouvé. Utilisez  \"!quest generate\" Pour en créer une")
        await tmpMsg.delete(delay=10)
        return
    questMessageIDs = Get_Quest_Var(fileName, "messageID").split('\\')
    for questMessageID in questMessageIDs:
        questMsg =  await message.channel.fetch_message(int(questMessageID))
        await questMsg.delete()
    os.remove(fileName)

################## TECHNICAL STUFF

def Generate_Table(fileName, nbDay, noEmpty, firstday=datetime.date.today()):
    sessionDict = Get_Event_Dict(fileName)

    #[ v for k,v in my_dict.items() if 'Date' in k]
    tableArray = []
    tmpString = "```ini\n" + DELIMITER

    for j in range(0, nbDay):

        dayString = firstday + datetime.timedelta(days=j)
        dayString = dayString.strftime("%d/%m/%y")
        dayList = [ v for k,v in sessionDict.items() if dayString in k]
        if not dayList:
            if not(noEmpty):
                tmpString += Generate_Empty_Day(dayString)
        else:
            for dayEvent in dayList:
                tmpString += Generate_Day(dayEvent[0], dayEvent[1], dayEvent[2], dayEvent[3], dayEvent[4], dayEvent[5:])
                tmpString += DELIMITER
        if (j+1)%7 == 0 and j+1<nbDay:
            tmpString += DELIMITER + "```\n"
            tableArray.append(tmpString)
            tmpString = "```ini\n" + DELIMITER

    tmpString += DELIMITER + "```\n"
    tableArray.append(tmpString)
    return tableArray

def Generate_Empty_Day(date):
    tmpString = "| %s |              ❌ VIDE ❌                         |\n" % date
    return tmpString

def Generate_Day(date, hour, nameRPG, maxPlayer, mj, playerList):
    tmpString = DELIMITER
    tmpString += "|[%s]| %s | %s | %s | %s |\n" % (date, hour.ljust(5), nameRPG.ljust(20)[:20], maxPlayer.ljust(2), only_ascii(bot.client.get_user(int(mj)).display_name).ljust(12)[:12])
    tmpString += DELIMITER
    tmpString += Generate_Player_Table(playerList)
    return tmpString

def Generate_Player_Table(playerList):
    tmpString = "| "
    listLen = len(playerList)
    if listLen == 0:
        tmpString += "".ljust(12*5) + "|\n"
        return tmpString
    for i in range(0,listLen):
        try:
            tmpString += only_ascii(bot.client.get_user(int(playerList[i])).display_name).ljust(11)[:11] + " "
        except :
            tmpString += "Joueur_ext  "
        
        if (i+1)%5 == 0 and i<listLen-1:
            tmpString += "|\n| "
    if listLen%5 ==0:
        tmpString += "|\n"
    else:
        tmpString += "".ljust(12*(5- listLen%5)) + "|\n"
    return tmpString

def Generate_New_DB(fileName, messageIDArray, nbDay, noEmpty):
    with open(fileName, "w", encoding="UTF-8") as fileP:
        fileP.write("#messageID=" + "\\".join(messageIDArray) + "\n")
        fileP.write("#nbDay=" + str(nbDay) + "\n")
        fileP.write("#noEmpty=" + str(noEmpty) + "\n")

def Get_Parameters(message):
    paramDict = dict()
    paramList = shlex.split(message)
    flag = True
    while len(paramList):
        if paramList[0].lower() == "+event" or paramList[0].lower() == "+e":
            paramDict["type"] = 1
        elif paramList[0].lower() == "+play" or paramList[0].lower() == "+p":
            paramDict["type"] = 2
        elif paramList[0].lower() == "-event" or paramList[0].lower() == "-e":
            paramDict["type"] = 3
        elif paramList[0].lower() == "-play" or paramList[0].lower() == "-p":
            paramDict["type"] = 4
        elif paramList[0].lower() == "generate":
            paramDict["type"] = 5
        elif paramList[0].lower() == "update":
            paramDict["type"] = 6
        elif paramList[0].lower() == "remove":
            paramDict["type"] = 7
        elif paramList[0].lower() == "-date" or paramList[0].lower() == "-d":
            if len(paramList)>1:
                paramDict["date"] = Get_Date(paramList[1])
                paramList.pop(1)
                if paramDict["date"] is None:
                    return None
            else:
                return None
        elif paramList[0].lower() == "-heure" or paramList[0].lower() == "-h" or paramList[0].lower() == "-hour":
            if len(paramList)>1:
                paramDict["hour"] = Get_Hour(paramList[1])
                paramList.pop(1)
                if paramDict["hour"] is None:
                    return None
            else:
                return None
        elif paramList[0].lower() == "-name" or paramList[0].lower() == "-n":
            if len(paramList)>1:
                paramDict["name"] = paramList[1]
                paramList.pop(1)
                if paramDict["name"] is None:
                    return None
            else:
                return None
        elif paramList[0].lower() == "-max" or paramList[0].lower() == "-m" or paramList[0].lower() == "-maximum":
            if len(paramList)>1:
                paramDict["max"] = only_numerics(paramList[1])
                paramList.pop(1)
                if paramDict["max"] is None:
                    return None
            else:
                return None
        elif paramList[0].lower() == "-mj" or paramList[0].lower() == "-gm":
            if len(paramList)>1:
                paramDict["mj"] = Get_User(paramList[1])
                paramList.pop(1)
                if paramDict["mj"] is None:
                    return None
            else:
                return None
        elif Get_Date(paramList[0]) is not None:
                paramDict["date"] = Get_Date(paramList[0])
        elif Get_Hour(paramList[0]) is not None:
                paramDict["hour"] = Get_Hour(paramList[0])
        else:
            return None
        paramList.pop(0)
        print(paramList)

    return paramDict

def Get_Quest_Var(fileName, varName):
    with open(fileName, "r", encoding="UTF-8") as fileP:
        line = fileP.readline()
        getString = "#" + varName + "="

        while line:

            if line.lower().startswith(getString.lower()):
                return line[len(getString):-1]
            line = fileP.readline()
    return ""

def Get_Event_Dict(fileName):
    sessionDict = dict()
    if os.path.exists(fileName):
        with open(fileName, "r", encoding="UTF-8") as fileP:
            fileLines = fileP.readlines()

        for i in range(0, len(fileLines)):
            if fileLines[i].startswith("#") or fileLines[i].startswith("\n"):
                continue
            lineArray = fileLines[i].split("\\")[:-1]
            sessionDict[lineArray[0] + lineArray[1] + lineArray[4]] = lineArray
    return sessionDict

def Set_Event_Dict(fileName, eventDict):
    
    newFileLine = []
    if os.path.exists(fileName):
        with open(fileName, "r", encoding="UTF-8") as fileP:
            fileLine = fileP.readline()
            while fileLine:
                if fileLine.startswith("#"):
                    newFileLine.append(fileLine)
                else:
                    break
                fileLine = fileP.readline()

    for key, value in eventDict.items():
        newString = value[0] + "\\" + value[1] + "\\" + value[2] + "\\" + value[3] + "\\" + value[4]
        if len(value)>5:
            for playerName in value[5:]:
                newString += "\\" + playerName
        newString += "\\\n"
        newFileLine.append(newString)

    with open(fileName, "w", encoding="UTF-8") as fileP:
        fileP.writelines(newFileLine)

def Set_Quest_Var(fileName, varName, varVal):
    with open(fileName, "r", encoding="UTF-8") as fileP:
        fileLines = fileP.readlines()

    getString = "#" + varName + "="

    for i in range(0, len(fileLines)):
        if fileLines[i].lower().startswith(getString.lower()):
            fileLines[i] = getString + varVal + "\n"
            break

    with open(fileName, "w", encoding="UTF-8") as fileP:
        fileP.writelines(fileLines)

def only_numerics(seq):
    seq_type= type(seq)
    return seq_type().join(filter(seq_type.isdigit, seq))

def only_ascii(seq):
    seq_type= type(seq)
    printable = set(string.printable)
    return seq_type().join(filter(lambda x: x in printable, seq))

def Get_Hour(string):
    try:
        return datetime.datetime.strptime(string, "%Hh%M").strftime("%Hh%M")
    except ValueError:
        pass
    try:
        return datetime.datetime.strptime(string, "%H:%M").strftime("%Hh%M")
    except ValueError:
        pass
    return None

def Get_Date(string):
    try:
        datetimeVal = parse(string, dayfirst=True)
        if datetimeVal.date() != datetime.datetime.today().date():
            return parse(string, dayfirst=True).strftime("%d/%m/%Y")
        else:
            return None
    except ValueError:
        return None

def Get_User(string):
    tmpstr = only_numerics(string)
    if bot.client.get_user(int(tmpstr)) is not None:
        return tmpstr
    else:
        return None

def is_same_user(user, username, discriminator):
    if user.name == username and user.discriminator == discriminator:
        return True
    else:
        return False

async def Send_Tmp_Message(channel, string, time):
    try:
        tmpMsg = await asyncio.wait_for(channel.send(string), timeout=5.0)
        await asyncio.wait_for(tmpMsg.delete(delay=time), timeout=5.0)
    except asyncio.TimeoutError:
        print('Timout trying to send or delete the message: ' + string)
    return

async def Send_Not_Admin_Message():
    return await asyncio.create_task(Send_Tmp_Message(message.channel, "Vous n'êtes pas administrateur !", TMPMESSAGETIMER))
