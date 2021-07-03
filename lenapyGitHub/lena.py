###########################################################
# Importations :

import discord, math, random, datetime, asyncio, gestion, os, emoji, donnes
from discord.ext import commands, tasks
from datetime import datetime, timedelta

###########################################################
# Initialisations des variables de bases :
bot, couleur, botID = commands.Bot(command_prefix = "l!", description= "LenaPy par LenaicU"),0x94D4E4,623211750832996354

tabArmeShot,tabArmeShotURL = donnes.lanceurNameList, gestion.LecFich("Donnees/Armes/lanceurURL.txt") #Lanceur
tabArmeBlast,tabArmeBlastURL = donnes.blasterNameList, gestion.LecFich("Donnees/Armes/blasterURL.txt") #Blaster
tabArmeRoller,tabArmeRollerURL = donnes.rolerNameList, gestion.LecFich("Donnees/Armes/rouleauURL.txt") #Rouleau
tabArmeBrush,tabArmeBrushURL = donnes.brushNameList, gestion.LecFich("Donnees/Armes/brushURL.txt") #Epinceau
tabArmeSnipe,tabArmeSnipeURL = donnes.fusilNameList, gestion.LecFich("Donnees/Armes/fusilURL.txt") #Snipe
tabArmeSeau,tabArmeSeauURL = donnes.slosherNameList, gestion.LecFich("Donnees/Armes/seauURL.txt") #Seau
tabArmeBadi,tabArmeBadiURL = donnes.badiNameList, gestion.LecFich("Donnees/Armes/badiURL.txt") #Badi
tabArmedualies,tabArmedualiesURL = donnes.dualiesNameList, gestion.LecFich("Donnees/Armes/dualiesURL.txt") #Double
tabArmePara,tabArmeParaURL = donnes.paraNameList, gestion.LecFich("Donnees/Armes/paraURL.txt") #Para

emojiList = [emoji.one,emoji.two,emoji.three,emoji.four,emoji.five,emoji.six,emoji.seven,emoji.eight,emoji.nine]

##########################################################
# Check
def errorCooldown(ctx,errorID,deltaT,TOr):
    # Enregistre dans ./Donnees/errors/{ctx.guild.id} la nature de l'erreur ainsi que la durée de cooldown restant
    if not os.path.exists("./Donnees/errors/"):
        os.mkdir("./Donnees/errors/")

    fich = open(f"./Donnees/errors/{ctx.guild.id}","w")
    fich.write(f"{errorID}\n{deltaT}\n{TOr}")
    fich.close()

def errorMe(ctx,errorID):
    # Enregistre dans ./Donnees/errors/{ctx.guild.id} la nature de l'erreur
    if not os.path.exists("./Donnees/errors/"):
        os.mkdir("./Donnees/errors/")

    fich = open(f"./Donnees/errors/{ctx.guild.id}","w")
    fich.write(f"{errorID}")
    fich.close()


async def cooldown30(ctx):
    "Vérifie si la commande a été utilisée par l'utilisateur durant les (Nombre) dernières secondes\n\nParamètre :\nNombre : int\n\nRenvoie :\nBool"

    guildID = ctx.guild.id
    if not os.path.exists(f"./Donnees/cooldown/{guildID}/"):
        os.mkdir(f"./Donnees/cooldown/{guildID}/")

    if not os.path.exists(f"./Donnees/cooldown/{guildID}/{ctx.command.name}.txt"):
        fich = open(f"./Donnees/cooldown/{guildID}/{ctx.command.name}.txt","w")
        fich.write(f"0\n{datetime(1,1,1,1,1,1,1)}")
        fich.close()

    fich = open(f"./Donnees/cooldown/{guildID}/{ctx.command.name}.txt","r")
    cooldownID,cooldownLastUse,userID = int(fich.readline()), datetime.strptime(fich.readline(), '%Y-%m-%d %H:%M:%S.%f'), ctx.author.id
    fich.close()

    if  userID != cooldownID:
        fich = open(f"./Donnees/cooldown/{guildID}/{ctx.command.name}.txt","w")
        fich.write(f"{userID}\n{datetime.now()}")
        fich.close()
        return True
    else:
        if datetime.now() - cooldownLastUse <= timedelta(seconds = 30):
            errorCooldown(ctx,"cooldownError",datetime.now() - cooldownLastUse,30)
            return False
        else:
            fich = open(f"./Donnees/cooldown/{guildID}/{ctx.command.name}.txt","w")
            fich.write(f"{userID}\n{datetime.now()}")
            fich.close()
            return True

async def isOwner(ctx):
    if ctx.author.id == 213027252953284609:
        return True
    else:
        errorMe(ctx,"notOwner")
        return False

##########################################################
# Mise en route

@bot.event
async def on_ready():
    print("\nLa phase d'initialisation est terminée, le bot est up !")
    await bot.change_presence(activity = discord.Game("l!aide"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        # Erreur d'argument
        await ctx.send("Je suis désolée mais il me manque des arguments")
    elif isinstance(error, commands.CommandNotFound):
        # Erreur de commande
        await ctx.send("J'ai beau chercher je ne trouve pas cette commande désolée. Essaye l!aide pour avoir la liste des commandes !")
    elif isinstance(error, commands.errors.MissingPermissions):
        # L'utilisateur n'a pas les bonnes permissions
        await ctx.send("Tu n'as pas les permissions necessaires pour cette commande désolée")
    elif str(error) == "Command raised an exception: TimeoutError: ":
        # L'utilisateur n'a pas répondu
        await ctx.send("Tu as mis trop de temps à répondre désolée")
    elif str(error).startswith("Command raised an exception: UnicodeEncodeError:"):
        # Un caractère inconnu n'a pas pu être enregistré
        await ctx.send("Une erreur de caractère est survenue. Je ne peux pas enregistrer d'emoji")
    elif str(error) == 'Command raised an exception: ValueError: day is out of range for month':
        # Le jour donné est trop grand pour le mois
        await ctx.send("Tu as du t'emmêler les pinceaux. La date du jour que tu m'a donné dépasse 31")
    elif isinstance(error, commands.errors.CheckFailure) and os.path.exists(f"./Donnees/errors/{ctx.guild.id}"):
        fich = open(f"./Donnees/errors/{ctx.guild.id}","r")
        content = fich.readlines()
        fich.close()

        if content[0].startswith("cooldownError"):
            content[1],content[2] = int(datetime.strptime(content[1][:-1],"%H:%M:%S.%f").second), int(content[2])
            temp = (1-(content[1]/content[2]))*100 # % d'avancement du cooldown
            temp2 = 100/len(emoji.clock)
            await ctx.message.add_reaction(emoji.clock[int(temp//temp2)])
        elif content[0].startswith("notOwner"):
            await ctx.message.add_reaction(emoji.cross)

    else:
        await ctx.send(f"Une erreur est survenu désolée. J'envoie un rapport à Léna")
        channel = discord.Client.get_channel(bot,808394788126064680)
        await channel.send(f"====================================================\n__{datetime.now()} , {ctx.guild.name} , {ctx.channel.name}__\n{error}")

##########################################################
# Commandes

@bot.command()
async def invite(ctx):
    inviteEm = discord.Embed(title = "Invitation", description = "Tu peux cliquer sur le lien ci-dessus pour m'inviter sur un de tes serveurs", url = "https://discord.com/api/oauth2/authorize?client_id=623211750832996354&permissions=124992&scope=bot", color = couleur)
    await ctx.send(embed = inviteEm)

@bot.command()
async def serverInfo(ctx):
    server = ctx.guild
    serverName = server.name
    nbrTxtChannels,nbrVocChannels,nbrPeople = len(server.text_channels),len(server.voice_channels),server.member_count 
    
    comNbrSalon = ""
    if nbrTxtChannels + nbrVocChannels > 30:
        comNbrSalon = "Ça fait beaucoup là non ?"
    
    message = f"Il y a {nbrPeople} personne sur {serverName} aujourd'hui\nIl y a également {nbrTxtChannels} salons écrits et {nbrVocChannels} salons vocaux {comNbrSalon}"
    await ctx.send(message)

@bot.command()
async def roll(ctx,diceType = str(100),nbr = str(1)):
    error,comB = [False],""
    if diceType.isdigit():
        dice = int(diceType)
    else:
        error[0] = True
        error = error + ["Hum... j'ai besoin que tu me donnes un nombre pour cela"]

    if nbr.isdigit():
        nbr = int(nbr)
    else:
        error[0] = True
        error = error + ["Hum... j'ai besoin de savoir combien de lancer tu veux que je fasse"]

    if not error[0]:
        a = False
        for b in [2,4,6,8,10,12,20,50,100]:
            if b == dice:
                a = True
                break
        if not a and dice > 1:
            comB = "Pas très conventionnel comme dé ça..."
        elif not a:
            error[0]=True
            error = error + ["Ton nombre doit être supérieur à 1"]

    if not error[0] and nbr == 1:
        com,comA,comE="","","!"
        result = random.randint(1,dice)
        if dice == 2:
            if result == 1:
                com = "Pile"
            else:
                com = "Face"
        elif dice == 20:
            if result == 1:
                com = "Eeet c'est un échec critique"
        elif dice == 100:
            if result <= 5:
                com = "Ow pas mal"
            elif result >= 95:
                com = "Et bah..."
        
        alea = random.randint(1,20)
        if alea <=3 and dice >2:
            comA = "Ah zut les dés sont tombés... Bon du coup... "
        elif alea <=3 and dice==2:
            comA = "Ah zut la pièce est tombée... Bon du coup... "
        elif alea < 7:
            comA = "Du coup... "
        elif alea > 6 and alea < 10:
            comA = "Les dés ont dit... "
        elif alea > 17:
            comA = "Alors alors..."

        alea = random.randint(1,500)
        if alea == 10 and dice == 2:
            await ctx.send("Heu... Comment dire... Tranche ?")
        else:
            alea = random.randint(1,6)
            if alea == 1:
                comE = "."
            elif alea == 5:
                comE = "..."
            await ctx.send(f"{comB}\n{comA}{result}{comE} {com}")
    elif not error[0] and nbr > 1:
        listRes = []
        resMsg = ""
        comp = 1
        while comp <= nbr:
            a = random.randint(1,dice)
            listRes += [a]
            resMsg += f"{a}\n"
            comp += 1

        await ctx.send(f"Du coup... voilà tes tirages (dés {dice}) :\n{resMsg}")
    else:
        await ctx.send(error[1])

@bot.command()
async def inktober(ctx,year = "any",day = "any"):
    inkTab2016=[[1,"Fast"],[2,"Noisy"],[3,"Collect"],[4,"Hungry"],[5,"Sad"],[6,"Hidden"],[7,"Lost"],[8,"Rock"],[9,"Broken"],[10,"Jump"],[11,"Transport"],[12,"Worried"],[13,"Scared"],[14,"Tree"],[15,"Relax"],[16,"Wet"],[17,"Battle"],[18,"Escape"],[19,"Flight"],[20,"Squeeze"],[21,"Big"],[22,"Little"],[23,"Slow"],[24,"One Dozen"],[25,"Tired"],[26,"Box"],[27,"Creepy"],[28,"Burn"],[29,"Surprise"],[30,"Wreck"],[31,"Friend"]]
    inkTab2017=[[1,"Swift"],[2,"Divided"],[3,"Poison"],[4,"Underwater"],[5,"Long"],[6,"Sword"],[7,"Shy"],[8,"Crooked"],[9,"Screech"],[10,"Gigantic"],[11,"Run"],[12,"Shattered"],[13,"Teeming"],[14,"Fierce"],[15,"Mysterious"],[16,"Fat"],[17,"Graceful"],[18,"Filthy"],[19,"Cloud"],[20,"Deep"],[21,"Furious"],[22,"Trail"],[23,"Juicy"],[24,"Blind"],[25,"Ship"],[26,"Squeak"],[27,"Climb"],[28,"Fall"],[29,"United"],[30,"Found"],[31,"Mask"]]
    inkTab2018=[[1,"Poisonous"],[2,"Tranquil"],[3,"Roasted"],[4,"Spell"],[5,"Chicken"],[6,"Drooling"],[7,"Exhausted"],[8,"Star"],[9,"Precious"],[10,"Flowing"],[11,"Cruel"],[12,"Whale"],[13,"Guarded"],[14,"Clock"],[15,"Weak"],[16,"Angular"],[17,"Swollen"],[18,"Bottle"],[19,"Scorched"],[20,"Breakable"],[21,"Drain"],[22,"Expensive"],[23,"Muddy"],[24,"Chop"],[25,"Prickly"],[26,"Stretch"],[27,"Thunder"],[28,"Gift"],[29,"Double"],[30,"Jolt"],[31,"Slice"]]
    inkTab2019=[[1,"Ring"],[2,"Mindless"],[3,"Bait"],[4,"Freeze"],[5,"Build"],[6,"Husky"],[7,"Enchanted"],[8,"Frail"],[9,"Swing"],[10,"Pattern"],[11,"Snow"],[12,"Dragon"],[13,"Ash"],[14,"Overgrown"],[15,"Legend"],[16,"Wild"],[17,"Ornament"],[18,"Misfit"],[19,"Sling"],[20,"Tread"],[21,"Treasure"],[22,"Ghost"],[23,"Ancient"],[24,"Dizzy"],[25,"Tasty"],[26,"Dark"],[27,"Coat"],[28,"Ride"],[29,"Injured"],[30,"Catch"],[31,"Ripe"]]
    inkTab2020=[[1,"Fish"],[2,"Wisp"],[3,"Bulky"],[4,"Radio"],[5,"Blade"],[6,"Rodent"],[7,"Fancy"],[8,"Teeth"],[9,"Throw"],[10,"Hope"],[11,"Disgusting"],[12,"Slippery"],[13,"Dune"],[14,"Armor"],[15,"Outpost"],[16,"Rocket"],[17,"Storm"],[18,"Trap"],[19,"Dizzy"],[20,"Coral"],[21,"Sleep"],[22,"Chef"],[23,"Rip"],[24,"Dig"],[25,"Buddy"],[26,"Hide"],[27,"Music"],[28,"Float"],[29,"Shoes"],[30,"Ominous"],[31,"Crawl"]]
    inkTab=[[2016,inkTab2016],[2017,inkTab2017],[2018,inkTab2018],[2019,inkTab2019],[2020,inkTab2020]]

    if year == "any":
        year = random.randint(2016,2020)
    if day == "any":
        day = random.randint(1,31)

    year = int(year)
    day = int(day)

    theme = []
    echec = False
    for a in inkTab:
        if a[0]==year:
            theme = a[1]

    if theme == []:
        echec = True

    inkDate = datetime(year,10,day).date()
    dateNow = datetime(2001,7,4)
    dateNow = dateNow.today().date()

    if inkDate < dateNow:
        conjug="était"
    elif inkDate == dateNow:
        conjug="(aujourd'hui quoi) est"
    else:
        conjug="sera"
    if not echec:
        await ctx.send(f"Le thème du {day} octobre {year} {conjug} **\"{theme[day-1][1]}\"**")
    else:
        await ctx.send("Désolée, mais l'année donnée n'a pas été trouvée\nJ'ai un peu la flemme de chercher les thèmes avant ceux de 2016, l'Inktober ne les partageaient pas avec une image unique comme aujourd'hui")

@bot.command()
async def batonnets(ctx,arg1 = "play"):
    def checkMsg(message):
        return message.author == ctx.message.author and ctx.message.channel == message.channel
    if arg1 == "rules":
        ruleEm = discord.Embed(title = "**__Jeu du bâtonnets__**", color = couleur)
        ruleEm.add_field(name = "__Règle du jeu :__",value = "Il y a 20 bâtonnets au centre de la table\nChacun son tour, des deux joueurs retirent 1, 2 ou 3 bâtonnets selon leurs envies\nLe joueur qui retire le dernier bâtonnet perd la partie")
        await ctx.send(embed = ruleEm)

    elif arg1 == "play":
        game, emb, bat, turn, msg, lastL, lastP = True,False,20,1,None,"-","-"
        PlayerName = ctx.author.name
        Wins = [[PlayerName,None],["LenaPy",None]]
        Players = [PlayerName,"LenaPy"]
        NextPlay = PlayerName
        while game:
            s=""
            if bat > 1:
                s="s"
            gameEm = discord.Embed(title = "**__Jeu du bâtonnets__**", description = f"Tour n°{turn}\nBâtonnet{s} restant{s} : {bat}", color = couleur)
            count = 0
            batE = ""
            while count<bat:
                batE = batE+" |"
                count = count+1
            gameEm.add_field(name = "Table de jeu :",value = batE,inline = False)
            gameEm.add_field(name = PlayerName, value = lastP, inline = True)
            gameEm.add_field(name = "LenaPy", value = lastL, inline = True)

            instruction =""
            if NextPlay != "LenaPy":
                instruction="\nTu dois répondre par 1,2,3, ou Quit pour continuer"
            gameEm.add_field(name = "__En attente de :__", value = f"{NextPlay}{instruction}", inline = False)

            if not emb:
                msg = await ctx.send(embed = gameEm)
                emb = True
            else :
                await msg.edit(embed = gameEm)

            if NextPlay == PlayerName:
                repContent = "a"
                boucleInit = False
                while (not repContent.isdigit() or not boucleInit) and repContent != "Quit":
                    try:
                        rep = ((await bot.wait_for("message",timeout = 30, check = checkMsg)))
                        repContent = rep.content
                        await rep.delete()
                        for a in ["1","2","3"]:
                            if a == repContent:
                                boucleInit = True
                                break
                    except:
                        repContent = "Quit"

                    if (not repContent.isdigit() or not boucleInit) and repContent != "Quit":
                        await ctx.send("Tu es sensé(e) répondre 1,2,3, ou Quit")

                if repContent!="Quit":
                    rep = int(repContent)
                    lastP = rep
                    NextPlay = "LenaPy"
            else :
                await asyncio.sleep(random.random())

                if bat > 7:
                    rep = random.randint(1,3)
                elif bat <=7 and bat > 4:
                    rep = bat-4
                elif bat-1 > 0:
                    rep = bat-1
                else:
                    rep = 1

                lastL = rep
                NextPlay = PlayerName
            
            if repContent!="Quit":
                bat = bat - rep

                if bat <= 0:
                    if NextPlay == Players[1]:
                        Wins[0][1],Wins[1][1]=False,True
                    else:
                        Wins[0][1],Wins[1][1]=True,False
                    game=False
                else :
                    turn = turn + 1
            
            else :
                game=False

        resCol = 0x7f00ff
        draw = False
        if Wins[0][1]==True:
            resCol = 0x008000
            vic = Wins[0][0]
            los = Wins[1][0]
        elif Wins[1][1]==True:
            resCol = 0xFF0000
            vic = Wins[1][0]
            los = Wins[0][0]
        else:
            draw = True

        resEm = discord.Embed(title = "**__Jeu du bâtonnet__**",description = "Résultats :", color = resCol)
        if not draw:
            resEm.add_field(name = "**__Gagnant :__**", value = vic)
            resEm.add_field(name = "__Perdant :__", value = los)
        else:
            resEm.add_field(name = "__Egalitée__", value = "Partie annulée")

        await msg.edit(embed = resEm)
    else:
        await ctx.send("Hum... Les arguments valides pour cette commande sont \"rules\" et \"play\"")

@bot.command()
async def choose(ctx,*message):
    choBet = []
    temp = ""
    for a in message:
        for b in a:
            if b != "|":
                temp += b
            else:
                choBet += [temp]
                temp = ""
        temp += " "
    choBet += [temp]
    await ctx.send(f"Je doute que tu tiennes en compte mon avis mais je choisi *\"{random.choice(choBet)}\"*")

@bot.command()
@commands.check(cooldown30)
async def sp2(ctx,com = "aide",nbr = "1",*tier):
    cheak = True #Variable de vérification d'erreur. True = good
    def checkReact(reaction,user):
        return user == ctx.message.author and msg.id == reaction.message.id and user.id != botID

    if com == "arme":
        ####    l!sp2 arme      ####
        # Renvoie une arme du jeu.
        # Fait nbr tirages
        # Si tier est vide, tirer parmis toutes les catégories. Sinon, tirer parmit la catégorie spécifié
        ############################

        try:
            nbr = int(nbr)
        except:
            await ctx.send(f"Un nombre est attendu à la place de {nbr}")
            cheak = False

        if cheak:
            #Selection aléatoire
            tabArmeAll, tabArmeAllURL, trouve = [],[],False
            if gestion.empty(tier):
                tabArmeAll = tabArmeShot + tabArmeBlast + tabArmeRoller + tabArmeBrush + tabArmeSnipe + tabArmeSeau + tabArmeBadi + tabArmedualies + tabArmePara
                tabArmeAllURL = tabArmeShotURL + tabArmeBlastURL + tabArmeRollerURL + tabArmeBrushURL + tabArmeSnipeURL + tabArmeSeauURL + tabArmeBadiURL + tabArmedualiesURL + tabArmeParaURL
            else:
                tabCatDisp = [["lanceur",tabArmeShot,tabArmeShotURL],["blaster",tabArmeBlast,tabArmeBlastURL],["rouleau",tabArmeRoller,tabArmeRollerURL],["epinceau",tabArmeBrush,tabArmeBrushURL],["snipe",tabArmeSnipe,tabArmeSnipeURL],["seau",tabArmeSeau,tabArmeSeauURL],["badigeonneur",tabArmeBadi,tabArmeBadiURL],["double",tabArmedualies,tabArmedualiesURL],["para-encre",tabArmePara,tabArmeParaURL]]
                for a in tabCatDisp:
                    if a[0] == tier[0]:
                        tabArmeAll = a[1]
                        tabArmeAllURL = a[2]
                        trouve=True
                        break
                        
                if not trouve:
                    cheak = False
                    await ctx.send(f"La catégorie donnée n'est pas reconnue\nLes catéogories possibles sont : lanceur, blaster, rouleau, epinceau, snipe, seau, badigeonneur, double, para-encre")
                
            if nbr == 1:
                if cheak:
                    nbrAl = random.randint(0,len(tabArmeAll)-1)
                    arme, armeURL = tabArmeAll[nbrAl], tabArmeAllURL[nbrAl]

                    #Réponse
                    tabRep = ["Pour toi ce sera :","Alors...","Et donc...","Tu dois prendre :"]

                    if arme[0][-1] == "K":
                        color = 0x2F4F4F
                    else:
                        color = 0x94D4E4
                    repEmb = discord.Embed(title = tabRep[random.randint(0,len(tabRep)-1)], description = arme, color = color)
                    repEmb.set_image(url = armeURL)

                    await ctx.send(embed = repEmb)

            else:
                if cheak:
                    rep = discord.Embed(title = "Voila pour vous !", color = 0x94D4E4)
                    comp = 1
                    while comp <= nbr:
                        rep.add_field(name = f"Le joueur {comp} doit prendre :", value = tabArmeAll[random.randint(0,len(tabArmeAll)-1)],inline = False)
                        comp+=1

                    await ctx.send(embed = rep)

    elif com == "scrim":
        ####    l!sp2 scrim     ####
        # Renvoie un embed contenant 7 map/modes, contenant des emotes
        # Par un système de réaction, permet d'afficher à la place un autre embed avec une image, et d'en changer
        ############################

        def checkReactLibre(reaction,user):
            return msg.id == reaction.message.id and user.id != botID

        msg, page,scrimList,donnes.mapListIndex,donnes.modeListIndex,scrimModList = await ctx.send(embed = discord.Embed(title = "l!sp2 scrim", description = "Initialisation")),0,[],list(range(0,len(donnes.mapList))),list(range(0,len(donnes.modeList))),list(range(0,7))
        for a in range(0,7):
            temp = random.randint(0,len(donnes.mapListIndex)-1)
            scrimList += [donnes.mapListIndex[temp]]
            donnes.mapListIndex.remove(donnes.mapListIndex[temp])

        for a in range(0,5):
            if len(donnes.modeListIndex)-1 != 0:
                temp = random.randint(0,len(donnes.modeListIndex)-1)
                scrimModList[a] = donnes.modeListIndex[temp]
                donnes.modeListIndex.remove(donnes.modeListIndex[temp])
            else:
                scrimModList[a] = donnes.modeListIndex[0]

        scrimModList[4],scrimModList[5],scrimModList[6] = scrimModList[0],scrimModList[1],scrimModList[2]

        scrimEm, temp = discord.Embed(color = couleur),""
        sortie = False
        while not sortie:
            if page == 0:
                temp=""
                scrimEm = discord.Embed(title = "__Scrim BO7 :__",color = couleur,description = "Remportez 4 manches pour gagner !")
                for a in range(0,7):
                    temp += f"{donnes.modeIconEmoji[scrimModList[a]]} : {donnes.mapList[scrimList[a]]}\n"
                scrimEm.add_field(name = "__Map / Mode :__",value = temp,inline = False)
                await msg.edit(embed = scrimEm)
                await msg.clear_reactions()
                await msg.add_reaction(emoji.plus)

            else:
                scrimEm = discord.Embed(color = couleur)
                scrimEm.set_image(url = donnes.mapIcon[scrimList[page-1]])
                scrimEm.add_field(name = f"__Manche {page} :__",value = f"{donnes.modeList[scrimModList[page-1]]}\n{donnes.mapList[scrimList[page-1]]}",inline = False)
                scrimEm.set_thumbnail(url = donnes.modeIcon[scrimModList[page-1]])
                await msg.edit(embed = scrimEm)
                await msg.clear_reactions()
                for a in range(0,7):
                    if page != a+1:
                        await msg.add_reaction(emojiList[a])
                await msg.add_reaction(emoji.moins)

            try:
                react = await bot.wait_for('reaction_add',timeout = 600.0,check=checkReactLibre)
                if str(react[0]) == emoji.plus:
                    page = 1
                elif str(react[0]) == emoji.moins:
                    page = 0
                else:
                    for a in range(0,7):
                        if str(react[0]) == emojiList[a]:
                            page = a+1
            except:
                sortie = True
                scrimEm,temp = discord.Embed(color = couleur),""
                for a in range(0,7):
                    temp += f"{donnes.modeList[scrimModList[a]]} - {donnes.mapList[scrimList[a]]}\n"
                scrimEm.add_field(name = "__Map / Mode :__",value = temp,inline = False)
                await msg.edit(embed = scrimEm)
                await msg.clear_reactions()
    
    elif com == "map":
        ####    l!sp2 map   ####
        # Renvoie un embed avec une image et une icone
        # Par un système de réaction, permet de modifier l'embed
        ########################

        msg = await ctx.send(embed = discord.Embed(title = "l!sp2 map",description = "Initialisation..."))
        if nbr != "1":
            b = f"{nbr}"
            if not gestion.empty(tier):
                b +=f" {tier[0]}"

            modeIconIndex,donnes.modeIconEmojiIndex,mapCor,mapLayout,modeCode,modeNom,trouv = ['https://cdn.discordapp.com/emojis/810513139740573696.png?v=1']+donnes.modeIcon , [emoji.turf]+ donnes.modeIconEmoji,random.randint(0,len(donnes.mapList)-1),0,0,["Guerre de Territoire"]+donnes.modeList,False
            for a in range(0,len(donnes.mapList)):                
                if b == donnes.mapList[a]:
                    mapCor = a
                    trouv=True
            if not trouv:
                mapCor = random.randint(0,len(donnes.mapList)-1)
                trouv="La map n'a pas été trouvée. Une autre a été choisi aléatoirement\n"
            else:
                trouv=""
            
            sortie = False
            while not sortie:
                if mapCor > 12:
                    mapLayout = donnes.mapLayoutList2[mapCor-13]
                else:
                    mapLayout = donnes.mapLayoutList1[mapCor]

                mapEm = discord.Embed(title = donnes.mapList[mapCor], description = f"{trouv}{modeNom[modeCode]}",color = couleur)
                try:
                    mapEm.set_thumbnail(url = modeIconIndex[modeCode])
                    mapEm.set_image(url = mapLayout[modeCode])
                except:
                    await ctx.send(modeIconIndex[modeCode]+' , '+mapLayout[modeCode])
                await msg.edit(embed = mapEm)
                await msg.clear_reactions()

                for a in [emoji.backward_arrow,emoji.turf,emoji.zone,emoji.stand,emoji.bazookarpe,emoji.palourde,emoji.forward_arrow]:
                    await msg.add_reaction(a)

                try:
                    react = await bot.wait_for('reaction_add',timeout = 10.0,check=checkReact)

                    if str(react[0]) == emoji.backward_arrow:
                        if mapCor == 0:
                            mapCor = len(donnes.mapList)-1
                        else:
                            mapCor = mapCor-1
                        trouv=""

                    elif str(react[0]) == emoji.forward_arrow:
                        if mapCor == len(donnes.mapList)-1:
                            mapCor = 0
                        else:
                            mapCor += 1
                        trouv=""

                    else:
                        for a in range(0,len(donnes.modeIconEmojiIndex)):
                            if str(react[0]) == donnes.modeIconEmojiIndex[a]:
                                modeCode = a
                except:
                    sortie = True
                    await msg.clear_reactions()
        else:
            mapEm,temp = discord.Embed(title = "l!sp2 map",color = couleur),""
            for a in donnes.mapList:
                temp+=a+"\n"
            mapEm.add_field(name = "__Liste des maps :__",value = temp, inline = False)
            await msg.edit(embed = mapEm)

    #elif com == "bonus":
        ####    l!sp2 bonus     ####
        # Renvoie un embed avec un description et un field variant et contenants des emojis
        # Un système de réaction permet de le modifier
        ############################

    #    msg = await ctx.send(embed = discord.Embed(title = "l!sp2 bonus",description = "Initialisation..."))
    #    for a in range(0,len(donnes.bonusCom)):
    #        bonusCo = a
    #        bonusEm = discord.Embed(title = donnes.bonusNom[bonusCo], description = donnes.bonusCom[bonusCo][0], color = couleur)
    #        bonusEm.set_thumbnail(url = donnes.bonusURL[bonusCo])
    #        bonusEm.set_footer(text= "10 AP = 1 Main\n3 AP = 1 Sub")
    #        comp = 1
    #        while comp < len(donnes.bonusCom[bonusCo]):
    #            bonusEm.add_field(name = f'__{donnes.bonusCom[bonusCo][comp]}__', value = donnes.bonusCom[bonusCo][comp+1], inline = False)
    #            comp+=2
    #        await  ctx.send(embed = bonusEm)

    else:
        msg = await ctx.send(embed = discord.Embed(title = "l!sp2",description = "Initialisation..."))
        helpCmdList,page,helpCmdCom = ["l!sp2 arme (Nombre) (Catégorie)","l!sp2 scrim","l!sp2 map (Map)"],0,[["Renvoie une arme aléatoire\n","(Nombre) : Le nombre de tirage à faire. Par défaut, 1","(Catégorie) : La catégorie parmis laquelle tirer. Par défaut, toutes les catégories sont prisent en compte\n","Les catégories sont :\nlanceur, blaster, rouleau, epinceau, snipe, seau, badigeonneur, double, para-encre"],["Renvoie 7 combos de map/mode sur le modèle de l'ebtv\n","Un système de réaction permet de choisir si on voir les manches une par une ou non"],["Renvoie la carte de (map)\n","(map) : La map dont vous voulez voir la carte. Par défaut, revoie la liste des maps\n","Un système de réaction permet de sélectioner un mode, ou de changer de map"]]
        helpEm = discord.Embed(title = "l!sp2",color = couleur)
        helpEm.set_footer(text = "Les attribus entre [crochets] sont obligatoires. Ceux entre (parenthèses) sont optionnels.")

        sortie = False
        while not sortie:
            if page == 0:
                temp = ""
                for a in range(0,len(helpCmdList)):
                    temp+=f"[{a+1}] {helpCmdList[a]}\n"

                helpEm.add_field(name ="__Liste des commandes :__",value = temp)
                await msg.edit(embed = helpEm)
                for a in range(0,len(helpCmdList)):
                    await msg.add_reaction(emojiList[a])

                try:
                    react = await bot.wait_for('reaction_add',timeout = 10.0,check=checkReact)
                    for a in range(0,len(helpCmdList)):
                        if str(react[0]) == emojiList[a]:
                            page = a+1
                except:
                    await msg.clear_reactions()
                    sortie = True

            else:
                helpEm = discord.Embed(title = helpCmdList[page-1],color = couleur)
                helpEm.set_footer(text = "Les attribus entre [crochets] sont obligatoires. Ceux entre (parenthèses) sont optionnels.")
                temp = ""
                for a in helpCmdCom[page-1]:
                    temp += a+"\n"

                helpEm.add_field(name = f"__{helpCmdList[page-1]}__",value = temp)
                await msg.edit(embed = helpEm)
                await msg.clear_reactions()
                sortie = True

@bot.command()
@commands.has_permissions(manage_messages=True)
async def roster(ctx,rostName = "list",*rost1):
    def checkMsg(message):
        return message.author == ctx.message.author and ctx.message.channel == message.channel
    def checkReact(reaction,user):
        return user == ctx.message.author and msg.id == reaction.message.id and user.id != botID

    guildID,minFich = ctx.guild.id,3
    path = "./Roster/"+str(guildID)    

    if not os.path.exists(path):
        os.mkdir(path)
        print(f"Le dossier {str(guildID)} a été créé (commande roster)")
    else:
        print(f"Dossier {str(guildID)} chargé (commande roster)")

    ContentDir = os.listdir(path)

    if rostName =="list":
        if gestion.empty(ContentDir):
            await ctx.send("Aucun rosteur n'est enregistré sur ce serveur")

        else:
            listEm = discord.Embed(title = "**Liste des rosters**",color=couleur)
            for a in ContentDir:
                NbrMemRost = str(len(gestion.LecFich(path+"/"+str(a))))
                listEm.add_field(name = a[0:-4], value = str(int(NbrMemRost)-minFich) + " membres dans ce roster", inline=False)
            await ctx.send(embed = listEm)

    elif rostName == "create":
        if gestion.empty(rost1):
            await ctx.send("Veillez indiquer le nom du roster :")
            rep = await bot.wait_for("message",timeout = 30, check = checkMsg)
            rep=rep.content+".txt"
        else:
            rep = str(rost1[0])+".txt"

        try:
            fich = open(path+"/"+rep,"x")
            fich.write(f"FFFFFF\nhttps://www.citationbonheur.fr/wp-content/uploads/2017/08/placeholder-300x300.png\nPas de description renseignée\n")
            fich.close()
            print(f"Création du fichier {path}/{rep[0:-4]}.txt")
            await ctx.send(f'Le roster {rep[0:-4]} a été créé. Entrez la commande "l!roster edit {rep[0:-4]}" pour commencer à l\'éditier')
        except:
            await ctx.send("Ce nom est déjà utilisé pour un autre roster sur ce serveur. Veillez entrer un nom disponible")

    elif rostName == "delete":
        
        test = False
        if gestion.empty(rost1):
            await ctx.send("Veillez indiquer le nom du roster :")
            rep = await bot.wait_for("message",timeout = 30, check = checkMsg)
            rep=rep.content+".txt"
        else:
            rep = str(rost1[0])+".txt"
            test = True
                
        for a in ContentDir:
            if rep == str(a):
                test = True
                break

        if not test:
            await ctx.send(f"Il n'y a aucun roster du nom de {rep[0:-4]} sur ce serveur")

        else:
            msg = await ctx.send(f"Vous êtes sur le point de supprimer le roster {rep[0:-4]}. Êtes vous sûr(e) ?")
            test=True
            await msg.add_reaction(emoji.check)
            await msg.add_reaction(emoji.cross)
            react = await bot.wait_for('reaction_add',timeout = 10.0,check=checkReact)
            if str(react[0])==emoji.check:
                os.remove(path+"/"+rep)
                await ctx.send("Le rosteur a bien été supprimé")
            else:
                await ctx.send("Procédure annulée")
            await msg.delete()

    else:
        for a in ContentDir:
            succes = False
            if rostName+".txt" == a:
                if gestion.empty(rost1):
                    fich = gestion.LecFich(f"{path}/{rostName}.txt")

                    viewEm = discord.Embed(title = f"**{rostName}**",color=int(fich[0][0:-1],16), description = fich[2])
                    viewEm.set_thumbnail(url = fich[1])

                    temp=""
                    if len(fich)> minFich:
                        for a in fich[minFich:]:
                            comp, tabTemp, compTemp = -1,[],0
                            while comp < len(a):
                                if a[comp] == ",":
                                    tabTemp+=[a[compTemp:comp]]
                                    compTemp=comp+1
                                comp+=1

                            tabTemp+=[a[compTemp:]]

                            viewEm.add_field(name = f"__{tabTemp[0]}__", value = f"__Pseudo ingame__ : {tabTemp[1]}\n__C.A.__ : {tabTemp[2]}\n", inline = False)
                    else:
                        viewEm.add_field(name = "Aucun joueurs !",value = f"Il n'y a pas encore de joueurs dans ce roster ! Rajoute en avec la commande \"l!roster {rostName} add\"")
                    
                    await ctx.send(embed = viewEm)
                    succes = True

                elif rost1[0] == "add":                    
                    if len(rost1)>1:
                        fich=gestion.LecFich(f"{path}/{rostName}.txt")
                        nameMention = ctx.message.mentions[0].name
                        for a in fich:
                            if nameMention == a[0:-1]:
                                await ctx.send(f"{nameMention} est déjà inscrit à ce roster !")
                                break
                            else:
                                addFich=open(f"{path}/{rostName}.txt","a")
                                temp=nameMention

                                if len(rost1)<4:
                                    await ctx.send("Veillez indiquer le pseudonyme in-game du joueur :")
                                    rep = await bot.wait_for("message",timeout = 30, check = checkMsg)
                                    temp=f"{temp},{rep.content}"

                                    await ctx.send("Veillez indiquer le CA du joueur (Sous le format : 1111-2222-3333)")
                                    rep = await bot.wait_for("message",timeout = 30, check = checkMsg)
                                    temp=f"{temp},{rep.content}"

                                elif len(rost1) == 4:
                                    temp=f"{nameMention},{rost1[2]},{rost1[3]}"

                                try:
                                    addFich.write(temp+"\n")
                                    addFich.close()
                                    await ctx.send(f"Le joueur {nameMention} a été rajouté au roster !")
                                except:
                                    addFich.close()
                                    os.remove(f"{path}/{rostName}.txt")
                                    await ctx.send("Une erreur est survenue. Je ne peux pas enregistrer d'émojis")
                                break       
                    succes = True    

                elif rost1[0] == "remove":                    
                    fich=gestion.LecFich(f"{path}/{rostName}.txt")
                    pos,test=2,False

                    while pos < len(fich):
                        nameMention= ctx.message.mentions[0].name

                        if fich[pos].startswith(nameMention):
                            msg = await ctx.send(f"Voulez-vous vraiment supprimer {nameMention} de {rostName}")
                            await msg.add_reaction(emoji.check)
                            await msg.add_reaction(emoji.cross)
                            react = await bot.wait_for('reaction_add',timeout = 10.0,check=checkReact)

                            if str(react[0]) == emoji.check:
                                if len(fich)-1==minFich:
                                    os.remove(f"{path}/{rostName}.txt")
                                    await ctx.send("Le rosteur a été supprimé (Plus aucun joueur)")
                                else:
                                    temp = fich[0]+fich[1]+fich[2]+"\n"
                                    for a in fich[minFich:]:
                                        if a != fich[pos]:
                                            temp+=a+"\n"
                                        
                                    fichTemp=open(f"{path}/{rostName}.txt","w")
                                    fichTemp.write(temp)
                                    fichTemp.close()
                                    await ctx.send(f"{nameMention} a été supprimé")
                                    test = True
                                break
                            else:
                                await ctx.send("La procédure a été annulée")
                            await msg.delete()
                            test = True
                        pos+=1
                    if not test:
                        await ctx.send("Je n'ai pas trouvé cette personne dans le roster désolée")
                    succes = True

                elif rost1[0] == "edit":                    
                    fich=gestion.LecFich(f"{path}/{rostName}.txt")
                    test, rostNameTemp, fichColorTemp = True, rostName, fich[0]
                    while test:
                        viewEmTemp = discord.Embed(title = f"**{rostNameTemp} (Prévisualitation)**",color=int(fich[0],16), description = fich[2])
                        viewEmTemp.set_thumbnail(url = fich[1])

                        temp=""
                        if len(fich)> minFich:
                            for a in fich[minFich:]:
                                comp, tabTemp, compTemp = -1,[],0
                                while comp < len(a):
                                    if a[comp] == ",":
                                        tabTemp+=[a[compTemp:comp]]
                                        compTemp=comp+1
                                    comp+=1

                                tabTemp+=[a[compTemp:]]
                                viewEmTemp.add_field(name = f"__{tabTemp[0]}__", value = f"__Pseudo ingame__ : {tabTemp[1]}\n__C.A.__ : {tabTemp[2]}\n", inline = False)
                        else:
                            viewEmTemp.add_field(name = "Aucun joueurs !",value = f"Il n'y a pas encore de joueurs dans ce roster ! Rajoute en avec la commande \"l!roster {rostName} add\"")

                        try:
                            await ctx.send(f"Voici la prévisualisation du roster {rostNameTemp}. Que voulez vous modifier ? (Répondre par Nom, Icone, Description, Couleur. Si vous en avez fini, ne répondez pas pendant 30 secondes)",embed = viewEmTemp)
                        except:
                            await ctx.send("Un des précédentes modification n'est pas passée.")
                            rep,test="none",False

                        try:    
                            rep = await bot.wait_for("message",timeout = 30, check = checkMsg)
                            rep=rep.content
                        except:
                            rep="none"
                            await ctx.send("Enregistrement des modifications en cour...")
                            if rostName != rostNameTemp:
                                fichier = open(path+"/"+rostNameTemp+".txt","w")
                                if fich[0] != fichColorTemp:
                                    fichier.write(fich[0]+"\n")
                                else:
                                    fichier.write(fich[0])
                            
                                for a in fich[1:]:
                                    fichier.write(a+"\n")

                                fichier.close
                                os.remove(path+"/"+rostName+".txt")
                            else:
                                fichier = open(path+"/"+rostName+".txt","w")
                                if fich[0] != fichColorTemp:
                                    fichier.write(fich[0]+"\n")
                                else:
                                    fichier.write(fich[0])

                                for a in fich[1:]:
                                    fichier.write(a+"\n")

                                fichier.close
                            await ctx.send(f"Les modifications sur le roster {rostNameTemp} ont bien été enregistrées !")
                            test = False

                        if rep == "Nom":
                            await ctx.send(f"Le nom actuel du rosteur est {rostNameTemp}. Veuillez renseigner le nouveau nom :")
                            rostNameTemp = await bot.wait_for("message",timeout = 30, check = checkMsg)
                            rostNameTemp=rostNameTemp.content

                        elif rep == "Icone":
                            await ctx.send(f"Actuellement, l'icone du rosteur est celui-ci :\n{fich[1]}\n\nVeuillez renseigner le nouvel icone (dois-être un URL commençant par http(s)) :")
                            fich[1] = await bot.wait_for("message",timeout = 30, check = checkMsg)
                            fich[1] = fich[1].content

                        elif rep == "Description":
                            await ctx.send(f"Actuellement, la description du rosteur est la suivante :\n{fich[2]}\n\nVeuillez renseigner la nouvelle description :")
                            fich[2] = await bot.wait_for("message",timeout = 30, check = checkMsg)
                            fich[2] = fich[2].content

                        elif rep == "Couleur":
                            colorEm = discord.Embed(title = "Couleur", color = int(fich[0],16), description = f"La couleur actuelle du rosteur est actuellement celle-ci :\n{fich[00]}\n\nVeuillez rentrer le code Hexadécimal de la nouvelle couleur")
                            await ctx.send(embed = colorEm)
                            fich[0] = await bot.wait_for("message",timeout = 30, check = checkMsg)
                            fich[0] = fich[0].content
                    succes = True

        if not succes:
            helpEm = discord.Embed(title = "__l!roster : Menu d'aide__", color =couleur, description = "Cette commande necessite que l'utilisateur ai la permisson de gérer les messages")
            helpEm.add_field(name = "l!roster list",value = "Renvoie la liste de tous les rosters enregistrés sur ce serveur ainsi que leur nombre de membres\nUtilsé par défaut si aucun argument est donné", inline = False)
            helpEm.add_field(name = "l!roster create (Nom)",value ="Permet de créer un roster\nSi aucun argument est donné, le bot attendra que vous notiez le nom du nouveau roster dans votre prochain message\n",inline = False)
            helpEm.add_field(name = "l!roster delete (Nom)",value ="Permet de supprimer un roster\nUne confirmation sera demandée\nSi aucun argument est donné, le bot attendra que vous notiez le nom du rosteur à supprimer dans votre prochain messgae\n",inline = False)
            helpEm.add_field(name = "l!roster [Nom]", value ="Permet de visualiser le rosteur [Nom]",inline = False)
            helpEm.add_field(name = "l!roster [Nom] add [@joueur] (Nom ingame) (Code Ami)",value = "Permet de rajouter un [@joueur] au roster [Nom]\nSi (Nom ingame) ou (Code Ami) ne sont pas renseigné, le bot vous demandera dans les écrires dans votre prochain messgage. Vous pourrez également rajouter un réseau social si vous le voulez\n[@joueur] dois memtionner quelqu'un, (Code Ami) doit être au format 1111-1111-1111\n",inline=False)
            helpEm.add_field(name = "l!roster [Nom] remove [@joueur]",value = "Permet de retirer [@joueur] du rosteur [Nom]\nUne confirmation sera demandée\n[@joueur] dois mentionner quelqu'un\nSi le roster deviens vide, celui-ci sera supprimé\n",inline = False)
            helpEm.add_field(name = "l!roster [Nom] edit",value = "Permet d'éditer les informations d'un roster\n",inline = False)
            helpEm.set_footer(text = "Les attribus entre [crochets] sont obligatoires. Ceux entre (parenthèses) sont optionnels.")
            await ctx.send(embed = helpEm)              
        
@bot.command()
@commands.has_permissions(manage_channels=True)
async def patchnote(ctx,salon):
    if salon != "test":
        guildID = ctx.guild.id
        path = "./Donnees/patchnotes/"+str(guildID)    
        fich = open(path,"w")
        fich.write(str(ctx.message.channel_mentions[0].id))
        fich.close()
        await ctx.send(f"Les prochains patchnotes seront bien envoyés sur le salon {salon} !")

@bot.command()
@commands.check(isOwner)
async def patchSend(ctx):
    # Affichage du patchnote
    if not os.path.exists("./Donnees/patchnotes/"):
        os.mkdir("./Donnees/patchnotes/")
        print("Création de du fichier patchnotes")

    fich,success,fail = gestion.LecFich("./Donnees/patchnotes/patch.txt"),0,0
    patchEmb = discord.Embed(color = couleur)
    patchEmb.set_author(name="LenaPy par LenaicU")
    patchEmb.set_footer(text = "Faites l!aide pour voir l'intégralitée des commandes !")

    comp,temp = 1,""
    while comp < len(fich):
        temp+=fich[comp]+"\n"
        comp += 1

    patchEmb.add_field(name =f"**__Patch {fich[0]}__**", value = temp, inline = False)
        
    for a in os.listdir('./Donnees/patchnotes/'):
        if a != "patch.txt":
            fichList = gestion.LecFich('./Donnees/patchnotes/'+a)
            channel = discord.Client.get_channel(bot,int(fichList[0]))
            try:
                await channel.send(embed = patchEmb)
                success+=1
            except:
                fail+=1

    await ctx.send(f"Le patch a bien été envoyé dans {success} serveurs, et il y a eu {fail} échecs")

@bot.command()
async def remember(ctx, remArg, *remLast):
    ####    l!remember  ####
    # Une commande qui enregistre un texte ou une image sur un fichier du nom de user.ID
    # Permet de revoir les messages enregistrés grace à un embed regroupant tous les remembers de l'user par nom
    ########################

    def checkReact(reaction,user):
        return user == ctx.message.author and msg.id == reaction.message.id and user.id != botID
    path, userID = "./Donnees/remember/", str(ctx.author.id)

    fichUser = path + userID + ".txt"
    if not os.path.exists(path):
        os.mkdir(path)

    if remArg == "add":
        #### l!remember add ####
        # Rajoute une entrée au fichier user.ID. Le titre doit être renseigné en premier puis ensuite le texte ou l'url
        ########################

        if not(gestion.empty(remLast)):
        # La commande ne s'effectue pas si aucun argument est renseigné après remArg

            fich = open(fichUser, "a")
            if remLast[0].startswith("http"):
                # Vérification si remLast[0] n'est pas un lien, dans quel cas on refuse
                await ctx.send(f'Pour des soucis de clareté, je préfère ne pas mettre de lien comme nom')
            else:
                remMsg = gestion.cutStrToList(gestion.listToStr(remLast),"|")
                
                for a in range(0,len(remMsg)):
                    remMsg[a] = remMsg[a]+"|"

                fichTemp, nomCom = gestion.cutStrToList(gestion.listToStr(gestion.LecFich(fichUser)),"|"), False
                for a in range(0,len(fichTemp)):
                    if remMsg[0][:-1] == fichTemp[a]:
                        await ctx.send("Ce nom est déjà utilisé pour un autre de tes mémos")
                        nomCom = True
                
                if not nomCom:
                    fich.write(gestion.listToStr(remMsg)+"\n")
                    fich.close()
                    comp = len(gestion.LecFich(fichUser))
                    await ctx.send(f'Ton mémo a bien été enregistré à la position {comp-1} !')
        else:
            await ctx.send(f'Je m\'attendais à quelque chose après add...')
        
    elif remArg == "view":
        #### l!remember view    ####
        # Cherche si remLast correspond à un nom, si oui le renvoie directement
        # Si pas trouvé ou aucun remLast donné, renvoie la liste des msg enregistrés
        ############################

        crea = False
        try:
            fich = gestion.LecFich(fichUser)
            crea,lenFich = True, len(fich)
        except:
            await ctx.send("Il n'y a aucuns mémos enregistrés à ton nom")

        if crea:
            msg = await ctx.send(embed = discord.Embed(title = "l!remember",description = "Initialisation"))
            trouv = [False,0]
            if not gestion.empty(remLast):
                if remLast[0].isdigit():
                    trouv[1] = int(remLast[0])
                    if trouv[1] < lenFich and trouv[1] >= 0:
                        trouv[0] = True
                    else:
                        await ctx.send("Le numéro d'index que tu a donné n'est pas valide")

                else:
                    arg = gestion.listToStr(remLast)

                    for a in range(0,lenFich):
                        if fich[a].startswith(arg):
                            trouv = [True,a]

            if gestion.empty(remLast) or not trouv[0]:
                page,sortie =0,False
                while not sortie:
                    temp,comp,remEm = "",page*10,discord.Embed(title = f'__l!remember :__ {ctx.author.name}', color = couleur)
                    while comp < lenFich and comp < (page+1)*10:
                        temp+=f'[{comp}] {gestion.cutStrToList(fich[comp],"|")[0]}\n'
                        comp+=1

                    remEm.add_field(name = "__Liste des notes :__",value = temp,inline = False)
                    await msg.edit(embed = remEm)
                    await msg.clear_reactions()

                    if (page*10)-1>0:
                        await msg.add_reaction(emoji.backward_arrow)

                    if lenFich < (page+1)*10:
                        for a in range(0,lenFich-(page*10)):
                            await msg.add_reaction(emoji.count[a])
                    else:
                        for a in range(0,10): 
                            await msg.add_reaction(emoji.count[a])

                    if (page+1)*10 < lenFich:
                        await msg.add_reaction(emoji.forward_arrow)

                    try:
                        react = await bot.wait_for('reaction_add',timeout = 15.0,check=checkReact)
                        react = str(react[0])
                        if react == emoji.backward_arrow:
                            page = page-1
                        elif react == emoji.forward_arrow:
                            page = page+1
                        else:
                            for a in range(0,10):
                                if react == emoji.count[a]:
                                    trouv = [True,a+(page*10)]
                                    sortie = True
                    except:
                        await msg.clear_reactions()
                        sortie = True
        
            if trouv[0]:
                sortie = False
                while not sortie:
                    fich,temp, remEm = gestion.cutStrToList(gestion.LecFich(fichUser)[trouv[1]],"|"),"",discord.Embed(title = f"__l!remember view {ctx.author.name}__",color = couleur)
                    for a in fich[1:]:
                        if a.startswith("  http"):
                            remEm.set_image(url = a[2:])
                        else:
                            temp+=a+"\n"
                    if temp != "":
                        remEm.add_field(name = f"__{fich[0]}__",value = temp, inline = False)
                    await msg.edit(embed = remEm)
                    await msg.clear_reactions()

                    if trouv[1]-1 >= 0:
                        await msg.add_reaction(emoji.backward_arrow)
                    if trouv[1]+1 < lenFich:
                        await msg.add_reaction(emoji.forward_arrow)
                    await msg.add_reaction(emoji.poubelle)

                    try:
                        react = await bot.wait_for('reaction_add',timeout = 15.0,check=checkReact)
                        react = str(react[0])
                        if react == emoji.backward_arrow:
                            trouv[1] = trouv[1]-1
                        elif react == emoji.forward_arrow:
                            trouv[1] = trouv[1]+1
                        elif react == emoji.poubelle:
                            remEm,temp = discord.Embed(title = f"__l!remember view {ctx.author.name}__",color = 0xFF0000),""
                            for a in fich[1:]:
                                if a.startswith("  http"):
                                    remEm.set_image(url = a[2:])
                                else:
                                    temp+=a+"\n"
                            
                            if temp != "":
                                remEm.add_field(name = f"__{fich[0]}__",value = temp, inline = False)
                            remEm.add_field(name = '**__Attention !__**', value = '**Voulez vous vraiment effacer ce mémo ?**')
                            await msg.edit(embed = remEm)
                            await msg.clear_reactions()
                            await msg.add_reaction(emoji.check)
                            await msg.add_reaction(emoji.cross)

                            try:
                                react = await bot.wait_for('reaction_add',timeout = 15.0,check=checkReact)
                                react = str(react[0])

                                if react == emoji.check:
                                    fich = gestion.LecFich(fichUser)
                                    fich[0] = fich[0][:-1]

                                    os.remove(fichUser)

                                    fichier = open(fichUser,"w")
                                    temp=""
                                    fich.remove(fich[trouv[1]])
                                    print(fich)
                                    for a in fich:
                                        temp += a+"\n"
                                        
                                    fichier.write(temp)
                                    sortie = True
                                    fichier.close()
                                    await msg.edit(embed = discord.Embed(title = f"__l!remember view {ctx.author.name}__",description = "Votre mémo a bien été supprimé"))
                                    await msg.clear_reactions()
                            except:
                                await msg.clear_reactions()
                                sortie = True
                    except:
                        await msg.clear_reactions()
                        sortie = True            

    else:
        await ctx.send("Les arguments de cette commandes sont add ou view")

@bot.command()
async def aide(ctx):
    def checkReact(reaction,user):
        return user == ctx.message.author and msg.id == reaction.message.id and user.id != botID
    
    sortie,page = False,0
    pageTitle = ["Lenapy : Liste des commandes","Catégorie : Commandes générales","Catégorie : Tirage aléatoires","Catégorie : Splatoon","Catégorie : Autre"]
    catList = ["Commandes générales","Tirages aléatoires","Splatoon","Autre"]
    cmgGen,cmdGenDesc = ["l!invite","l!patchnote [#salon]","l!serverInfo"],["Envoie le lien d'invitation du bot","Nécessite la permission de gérer les salons\nPemrmet de définir le salon dans lequel seront envoyés les futurs patchnotes\n[#salon] : Salon textuel","Renvoie quelques informations sur le serveur actuel"]
    cmdAlea,cmdAleaCom = ["l!batonnets","l!choose [choix | choix]","l!roll (Dé) (Nombre)"],["Permet de jouer aux batonnets avec le bot","Permet de tirer aléatoirement une proposition\n[choix] : Les différentes propositions. Leurs nombres nombres ne sont pas limités. Doivent être séparées par \"|\"","Permet de lancer un tirage aléatoire entre 1 (inclu) et (Dé) (inclu)\n(Dé) : La valeur maximale du tirage. Par défaut, 100\n(Nombre) : Le nombre de tirage. Par défaut, 1"]
    cmdSp,cmdSpCom = ["l!sp2 arme","l!roster"],["Effectuez la commande l!sp2 aide pour voir la page d'aide détaillée de cette commande","Effectuez la commande l!roster aide pour voir la page d'aide détaillée de cette commande"]
    cmdAutre, cmdAutreCom = ["l!inktober (Année) (Jour)","l!remember add [titre] | (texte / image)","l!remember view (titre / nombre)"],["Renvoie le thème de l'inktober pour l'année et le jour spécifié\n(Année) : L'année voulu. Par défaut, en renvoie une aléatoire\n(Jour) : Le jour voulu. Par défaut, en renvoie un aléatoire","Permet de faire retenir quelque chose au bot pour vous\n[titre] : Le titre de votre mémo\n(texte) : Le contenu de votre memo\n(image) : Le lien de votre image\n\nLe titre, le texte et ou l'image doivent être séparés par un \"|\"\n\nExemple : l!remember add titre | url | text","Permet de voir les mémos enregistrés avec l!remember add ainsi que de les effacer\n\n(titre / nombre) : Permet de rechercher votre mémo grace à son titre ou sa position. Par défaut, renvoie la liste de tous vos mémos"]
    indexCat, indexCom = [catList,cmgGen,cmdAlea,cmdSp,cmdAutre],["0",cmdGenDesc,cmdAleaCom,cmdSpCom,cmdAutreCom]

    msg = await ctx.send(embed = discord.Embed(title = "l!aide", description = "Initialisation..."))

    while not sortie:
        init = discord.Embed(color = couleur)
        init.set_author(name = "LenaPy par LenaicU")

        ctn,temp = 0,""
        while ctn < len(indexCat[page]):
            temp+=f"[{ctn+1}] {indexCat[page][ctn]}\n"
            ctn+=1

        init.add_field(name = pageTitle[page], value = temp, inline = False)
        ctn = 0
        await msg.edit(embed = init)
        await msg.clear_reactions()
        while ctn < len(indexCat[page]):
            await msg.add_reaction(emojiList[ctn])
            ctn+=1

        try:
            react = await bot.wait_for('reaction_add',timeout = 20.0,check=checkReact)
            if page == 0:
                ctn = 0
                while ctn < len(catList):
                    if str(react[0]) == emojiList[ctn]:
                        page = ctn+1
                    ctn+=1
            else:
                ctn = 0
                while ctn < len(indexCat[page]):
                    if str(react[0]) == emojiList[ctn]:
                        helpEm = discord.Embed(color = couleur)
                        helpEm.set_author(name = "LenaPy par LenaicU")
                        helpEm.set_footer(text = "Les attributs entre [crochets] sont obligatoires. Ceux entre (parenthèses) sont optionnels")
                        helpEm.add_field(name = f"__{indexCat[page][ctn]}__", value = indexCom[page][ctn])
                        await msg.edit(embed = helpEm)
                        await msg.clear_reactions()
                        sortie = True
                        break
                    ctn+=1
        except:
            await msg.clear_reactions()
            sortie = True


##########################################################
# Démarrage du bot
bot.run("Privicy")