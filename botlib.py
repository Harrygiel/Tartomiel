import os
import discord
from jellyfish import jaro_winkler
def get_acronym(gamestring):
    return "".join(e[0] for e in gamestring.split())

def is_subname(source, target):
    index=-1
    #first letter is same
    if source[0].lower() != target[0].lower():
        print("Not same first letter")
        return False

    #every first letter of the target words is in the source
    for word in target.lower().split():
        found = False
        for i in range(len(source)):
            if word[0] == source[i].lower() and i > index:
                index = i
                found = True
                break
        if not found:
            print("Not every first letter of the target words is in the source")
            return False

    index=-1
    #every letters of the source is in the target, in this order
    for letter in source.lower():
        found = False
        for i in range(len(target)):
            if letter == target[i].lower() and i > index:
                index = i
                found = True
                break
        if not found:
            print("Not every letters of the source is in the target, in this order")
            return False

    return True

def new_playdb_line(userid, gamelist):
    newplayerline = str(userid)
    for game in gamelist:
        if game[0].isspace():
            game = game[1:]
        newplayerline += "," + game
    newplayerline += "\n"
    return newplayerline

def is_same_user(user, username, discriminator):
    if user.name == username and user.discriminator == discriminator:
        return True
    else:
        return False

def func_bonjour(message, client):
    if str(client.user.id) in message.content or not "<@!" in message.content:
        if is_same_user(message.author, "Harrygiel", "7564"):
            return 'Bonjour Créateur <@%s> !' % message.author.id
        elif is_same_user(message.author, "Berna", "2042"):
            return 'Bonjour <@%s>, Impératrice des crabes !' % message.author.id
        elif is_same_user(message.author, "EmpereurAmecareth", "4363"):
            return 'Bonjour Templier Noir <@%s> !' % message.author.id
        elif is_same_user(message.author, "Snaps", "3760"):
            return 'Bonjour Grand Master <@%s> !' % message.author.id
        elif is_same_user(message.author, "Réma", "0556"):
            return 'Bonjour roi des chieurs <@%s>, dieu des casse-couilles, grand chef des faignants et empereur des embêteurs de fille !' % message.author.id
        elif is_same_user(message.author, "Soja", "6345"):
            return 'Bonjour Maitresse <@%s> !' % message.author.id
        else:
            return 'Bonjour <@%s> !' % message.author.id

def func_gamelist(message, client):
    if message.content[1:].lower().startswith('call'):
        if message.content[6:].isupper() and not " " in message.content[6:]:
            print(message.content)
            acronym = True
        else:
            acronym = False
        gamecalled = message.content.lower()[6:]
        players = []
        with open("play.db", "r", encoding="UTF-8") as playdb:
            playline = playdb.readline()
            while playline:
                usergames = playline.replace("\n","").split(",")[1:]
                for usergame in usergames:
                    if acronym:
                        if gamecalled == get_acronym(usergame).lower():
                            gamecalled = usergame
                            players.append(playline.split(",")[0])
                            acronym = False
                        elif is_subname(gamecalled, usergame):
                            gamecalled = usergame
                            players.append(playline.split(",")[0])
                            acronym = False
                    else:
                        if jaro_winkler(gamecalled.lower().replace(" ",""), usergame.lower().replace(" ","")) > 0.9:
                            gamecalled = usergame
                            players.append(playline.split(",")[0])
                playline = playdb.readline()
        if players:
            msg = "Hey ! <@%s> veut jouer avec vous à %s " % (message.author.id, gamecalled)
            for player in players:
                msg += "<@%s> " % player
            return msg
        else:
            #Trying to find if any game is close enough to the called game
            with open("play.db", "r", encoding="UTF-8") as playdb:
                playline = playdb.readline()
                while playline:
                    usergames = playline.replace("\n","").split(",")[1:]
                    for usergame in usergames:
                        if jaro_winkler(gamecalled.lower().replace(" ",""), usergame.lower().replace(" ","")) > 0.8:
                            return "Personne ne joue à ce jeu :cry: Mais peut être vouliez vous dire %s ?" % usergame
                    playline = playdb.readline()
            
            return "Personne ne joue à ce jeu :cry:"

    elif message.content[1:].lower().startswith('play') or message.content.lower().startswith('unplay'):
        if message.content.lower().startswith('unplay'):
            removegame=True
            gamelist = message.content[8:].split(",")
        else:
            removegame=False
            gamelist = message.content[6:].split(",")

        with open("play.db", "r", encoding="UTF-8") as playdb:
            with open("play.db.tmp", "w", encoding="UTF-8") as playdbtmp:
                newline = None
                playline = playdb.readline()
                while playline:
                    if playline.startswith(str(message.author.id)):
                        #OLD USER
                        usergames = playline.replace("\n","").split(",")[1:]
                        for game in gamelist:
                            if removegame:
                                for usergame in usergames:
                                    if game.lower().replace(" ","") == usergame.lower().replace(" ",""):
                                        usergames.remove(usergame)
                                        break
                            else:
                                found = False
                                for usergame in usergames:
                                    if game.lower().replace(" ","") == usergame.lower().replace(" ",""):
                                        found = True
                                        break
                                if not found:
                                    usergames.append(game)

                        newline = new_playdb_line(message.author.id, usergames)
                        playdbtmp.write(newline)
                    else:
                        playdbtmp.write(playline)
                    playline = playdb.readline()

                if not newline:
                    #NEW USER
                    if removegame:
                        return "Vous n'êtes pas dans la base de donnée de jeu divers !"
                    newline = new_playdb_line(message.author.id, gamelist)
                    playdbtmp.write(newline)
        os.remove("play.db.old")
        os.rename("play.db", "play.db.old")
        os.rename("play.db.tmp", "play.db")
        gamelist = newline.split(",")[1:]
        returntxt = "Vous jouez maintenant à :\n"
        for game in gamelist:
            returntxt += game + "\n"

        return returntxt