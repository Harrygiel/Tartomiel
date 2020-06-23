import os
import datetime
import discord

def func_bonjour(message, client):
    if str(client.user.id) in message.content or not "<@!" in message.content:
        if is_same_user(message.author, "Harrygiel", "7564"):
            return 'Bonjour Créateur <@%s> !' % message.author.id
        else:
            return 'Bonjour <@%s> !' % message.author.id

async def Quest_Manager(message, client):
	messageBody = message.content[7:]
	fileName = "tableList/"+ str(message.channel.id) + ".txt"
	await message.delete(delay=30)

	if messageBody.lower().startswith('+event') or messageBody.lower().startswith('+e'):
		await Call_Create_Event(message, fileName)
		await Call_Update(message, fileName)
	elif messageBody.lower().startswith('-event') or messageBody.lower().startswith('-e'):
		await Call_Remove_Event(message, fileName)
		await Call_Update(message, fileName)
	elif messageBody.lower().startswith('generate'):
		await Call_Generate(message, fileName)
	elif messageBody.lower().startswith('update'):
		await Call_Update(message, fileName)
	elif messageBody.lower().startswith('remove'):
		await Call_Remove(message, fileName)
	else:
		await message.channel.send("Commande non reconnu") 



async def Call_Create_Event(message, fileName):
	messageBody = message.content[7:]
	questParameters = messageBody.split(" ")[1:]
	if len(questParameters)<5:
		tmpMsg = await message.channel.send("Ajouter un évènement demande plus de paramètre !")
		await tmpMsg.delete(delay=10)
		return

	sessionDict = Get_Event_Dict(fileName)
	if questParameters[0]+questParameters[1]+questParameters[4] in sessionDict:
		tmpMsg = await message.channel.send("L'évènement est déjà dans la table des quêtes !")
		await tmpMsg.delete(delay=10)
		return

	with open(fileName, "a") as fileP:
		fileP.write("\n" + questParameters[0] + "\\" + questParameters[1] + "\\" + questParameters[2] + "\\" + questParameters[3] + "\\" + questParameters[4] + "\\")
	tmpMsg = await message.channel.send("Evènement Ajouté!")
	await tmpMsg.delete(delay=10)
	return

async def Call_Remove_Event(message, fileName):
	messageBody = message.content[7:]
	questParameters = messageBody.split(" ")[1:]
	if len(questParameters)<3:
		tmpMsg = await message.channel.send("Supprimer un évenement demande plus de paramètre !")
		await tmpMsg.delete(delay=10)
		return

	sessionDict = Get_Event_Dict(fileName)
	if questParameters[0]+questParameters[1]+questParameters[2] in sessionDict:
		sessionDict.pop(questParameters[0]+questParameters[1]+questParameters[2])
		Set_Event_Dict(fileName, sessionDict)
		tmpMsg = await message.channel.send("Evènement supprimé!")
		await tmpMsg.delete(delay=10)
		return
	else:
		tmpMsg = await message.channel.send("L'évènement n'est pas dans la table des quêtes !")
		await tmpMsg.delete(delay=10)
		return

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
		tmpMsg = await message.channel.send("La table des quêtes a déjà été généré. Utilisez \"!quest remove\" pour la supprimer")
		await tmpMsg.delete(delay=10)
		return
	sent = await message.channel.send(Generate_Table(fileName, nbDay, noEmpty))
	Generate_New_DB(fileName, str(sent.id), str(nbDay), str(noEmpty))

async def Call_Update(message, fileName):
	questMessageID = Get_Quest_Var(fileName, "messageID")
	nbDay = int(Get_Quest_Var(fileName, "nbDay"))
	noEmpty = False
	if Get_Quest_Var(fileName, "noEmpty") == "True":
		noEmpty = True
	questMsg =  await message.channel.fetch_message(int(questMessageID))
	await questMsg.edit(content=Generate_Table(fileName, nbDay, noEmpty))

async def Call_Remove(message, fileName):
	if not(os.path.exists(fileName)):
		tmpMsg = await message.channel.send("Aucune table des quêtes n'a été trouvé. Utilisez  \"!quest generate\" Pour en créer une")
		await tmpMsg.delete(delay=10)
		return
	questMessageID = Get_Quest_Var(fileName, "messageID")
	questMsg =  await message.channel.fetch_message(int(questMessageID))
	await questMsg.delete()
	os.remove(fileName)

def Generate_Table(fileName, nbDay, noEmpty):
	sessionDict = Get_Event_Dict(fileName)

	#[ v for k,v in my_dict.items() if 'Date' in k]
	tmpString = "```ini\n+------------+-------+--------------------+----+--------------+\n"

	for j in range(0, nbDay):
		dayString = datetime.date.today() + datetime.timedelta(days=j)
		dayString = dayString.strftime("%d/%m/%y")
		dayList = [ v for k,v in sessionDict.items() if dayString in k]
		if not dayList:
			if not(noEmpty):
				tmpString += Generate_Empty_Day(dayString)
		else:
			for dayEvent in dayList:
				tmpString += Generate_Day(dayEvent[0], dayEvent[1], dayEvent[2], dayEvent[3], dayEvent[4], dayEvent[5:])
				tmpString += "+------------+-------+--------------------+----+--------------+\n"

	tmpString += "+------------+-------+--------------------+----+--------------+\n```\n"

	return tmpString

def Generate_Empty_Day(date):
	tmpString = "| %s |              ❌ VIDE ❌                         |\n" % date
	return tmpString

def Generate_Day(date, hour, nameRPG, maxPlayer, mj, playerList):
	tmpString = "+------------+-------+--------------------+----+--------------+\n"
	tmpString += "|[%s]| %s | %s | %s | %s |\n" % (date, hour.ljust(5), nameRPG.ljust(20)[:20], maxPlayer.ljust(2), mj.ljust(12)[:12])
	tmpString += "+------------+-------+--------------------+----+--------------+\n"
	tmpString += Generate_Player_Table(playerList)
	return tmpString

def Generate_Player_Table(playerList):
	tmpString = "| "
	listLen = len(playerList)
	if playerList[0] == "\n":
		tmpString += "".ljust(12*5) + "|\n"
		return tmpString
	for i in range(0,listLen):
		tmpString += playerList[i].ljust(11)[:11] + " "
		if (i+1)%5 == 0 and i<listLen-1:
			tmpString += "|\n| "
	if listLen%5 ==0:
		tmpString += "|\n"
	else:
		tmpString += "".ljust(12*(5- listLen%5)) + "|\n"
	return tmpString

def Generate_New_DB(fileName, messageID, nbDay, noEmpty):
	with open(fileName, "w", encoding="UTF-8") as fileP:
		fileP.write("#messageID=" + str(messageID) + "\n")
		fileP.write("#nbDay=" + str(nbDay) + "\n")
		fileP.write("#noEmpty=" + str(noEmpty) + "\n")

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
			lineArray = fileLines[i].split("\\")
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
		else:
			newString += "\\"
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