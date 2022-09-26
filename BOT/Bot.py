from BOT.Clock import *
from BOT.TimeTable import TimeTable
from BOT.importBot import t, d, a, os
from generique import *

false: t.List[str] = ['false', 'f', 'no', 'n', '0']
true: t.List[str] = ['true', 't', 'yes', 'y', '1']


########################################################################################################################
######################################## Class Bot(d.Client) ###########################################################
########################################################################################################################


class Bot(d.Client):
    """
    Class Bot(d.Client)
    Description:
        Cette classe est la classe principale du bot, elle hérite de la classe Client de la librairie discord.py
    Attributs:
        dataFolder: str
            le chemin du dossier de données
        keys: t.List[str]
            les clés du fichier de configuration
        CommandInit: str
            le caractère d'initialisation des commandes
        boolEvent: bool
            booléen qui permet de savoir si l'Event est lancé
        booltimeEvent: bool
            booléen qui permet de savoir si l'Event est lancé à une heure précise
        chanelEvent: d.TextChannel
            le channel dans lequel l'Event est lancé
        timerEvent: int
            le temps entre chaque lancement de l'Event
        clockEvent: Clock
            l'heure à laquelle l'Event est lancé
        timetable: TimeTable
            l'objet qui permet de récupérer l'emplois du temps
        fileSystem: JsonFile
            le fichier de configuration
    """
    dataFolder: str = './data/'
    keys: t.List[str] = ['CommandInit', 'boolEvent', 'booltimeEvent', 'chanelEvent', 'clockEvent', 'timerEvent']

    CommandInit: str = '!'
    boolEvent: bool = False
    booltimeEvent: bool = False
    chanelEvent: d.TextChannel = None
    clockEvent: Clock = Clock(heure=8, minute=0, seconde=0)
    timerEvent: int = 10  # 3600

    fileSystem: JsonFile = None
    timetable: TimeTable

    def __init__(self, url: str, *args, **kwargs) -> None:
        """
        Constructeur de la classe Bot
        Description:
            Constructeur de la classe Bot
        :param url: str -> L'url du bot
        :param args: t.List[str] -> Les arguments de la classe Client
        :param kwargs: t.Dict[str, str] -> Les arguments de la classe Client
        """
        if not os.path.exists(self.dataFolder[:-1]):
            os.mkdir(self.dataFolder[:-1])

        self.timetable = TimeTable(url=url, parentPath=self.dataFolder)
        super().__init__(*args, **kwargs)

    async def on_ready(self) -> None:
        """
        Fonction on_ready
        Description:
            Fonction qui est appelée lorsque le bot est prêt
        :return: None
        """
        self.verifConfig()
        print('Logged in as {0.user}'.format(self))
        await self.Event()

    async def on_message(self, message: d.Message) -> None:
        """
        Fonction on_message
        Description:
            Fonction qui est appelée lorsque le bot reçoit un message
        :param message: d.Message -> Le message reçu
        :return: None
        """
        if message.author == self.user:
            return
        if message.content.startswith(self.CommandInit + 'hello'):
            await message.channel.send('Hello ' + message.author.name + ' !')

        elif message.content.startswith('ping'):
            await message.channel.send('pong')

        elif message.content.endswith('quoi'):
            await message.channel.send('feur')

        elif message.content.startswith(self.CommandInit + 'iamAdmin'):
            await self.isAdmin(message, True)

        elif message.content.startswith(self.CommandInit + 'off'):
            await self.off(message=message)

        elif message.content.startswith(self.CommandInit + 'setCommandInit'):
            await self.setCommandInit(message=message)

        elif message.content.startswith(self.CommandInit + 'startEvent'):
            await self.startEvent(message=message)

        elif message.content.startswith(self.CommandInit + 'setChannelEvent'):
            await self.setChannelEvent(message=message)

        elif message.content.startswith(self.CommandInit + 'setTimeEvent'):
            await self.setTimeEvent(message=message)

        elif message.content.startswith(self.CommandInit + 'seeConfig'):
            await self.seeConfig(message=message)

    async def Event(self) -> None:
        """
        Fonction Event
        Description:
            Fonction qui est appelée lorsque l'Event est lancé
        :return: None
        """
        while not self.is_closed():
            if self.booltimeEvent:
                await a.sleep(10)
                while self.clockEvent.__inf__(whatTimeIsIt()) is False:
                    await a.sleep(1)
            else:
                await a.sleep(self.timerEvent)

            if self.boolEvent and self.chanelEvent is not None:
                self.timetable.__update__()
                if os.path.exists('file.png'):
                    await self.chanelEvent.send('Emplois du temps :')
                    await self.chanelEvent.send(file=d.File('TimeTable.png'))
                elif os.path.exists('TimeTable.png'):
                    await self.chanelEvent.send('Emplois du temps :')
                    await self.chanelEvent.send(file=d.File('self.dataFolderTimeTable.pdf'))
                elif os.path.exists(self.dataFolder + 'file.pdf'):
                    await self.chanelEvent.send('Emplois du temps :')
                    await self.chanelEvent.send(file=d.File(self.dataFolder + 'file.pdf'))
                else:
                    await self.chanelEvent.send('Emplois du temps')

    def writeCommandInit(self, w: bool = False) -> None:
        """
        Fonction writeCommandInit
        Description:
            Fonction qui permet d'écrire le caractère d'initialisation des commandes dans le fichier de configuration
        :return: None
        """
        if w:
            self.fileSystem.__setitem__("CommandInit", self.CommandInit)
        elif self.fileSystem.__getitem__("CommandInit") is None \
                or not isinstance(self.fileSystem.__getitem__("CommandInit"), str):
            self.fileSystem.__setitem__("CommandInit", self.CommandInit)
        else:
            self.CommandInit = self.fileSystem.__getitem__("CommandInit")

    def writeBoolEvent(self, w: bool = False) -> None:
        """
        Fonction writeBoolEvent
        Description:
            Fonction qui permet d'écrire le booléen de l'Event dans le fichier de configuration
        :return: None
        """
        if w:
            self.fileSystem.__setitem__("boolEvent", self.boolEvent)
        elif self.fileSystem.__getitem__("boolEvent") is None or \
                not isinstance(self.fileSystem.__getitem__("boolEvent"), bool):
            self.fileSystem.__setitem__("boolEvent", self.boolEvent)
        else:
            self.boolEvent = self.fileSystem.__getitem__("boolEvent")

    def writeBoolTimeEvent(self, w: bool = False) -> None:
        """
        Fonction writeBoolTimeEvent
        Description:
            Fonction qui permet d'écrire le booléen du temps de l'Event dans le fichier de configuration
        :return: None
        """
        if w:
            self.fileSystem.__setitem__("booltimeEvent", self.booltimeEvent)
        elif self.fileSystem.__getitem__("booltimeEvent") is None or \
                not isinstance(self.fileSystem.__getitem__("booltimeEvent"), bool):
            self.fileSystem.__setitem__("booltimeEvent", self.booltimeEvent)
        else:
            self.booltimeEvent = self.fileSystem.__getitem__("booltimeEvent")

    def writeTimerEvent(self, w: bool = False) -> None:
        """
        Fonction writeTimerEvent
        Description:
            Fonction qui permet d'écrire le timer de l'Event dans le fichier de configuration
        :return: None
        """
        if w:
            self.fileSystem.__setitem__("timerEvent", self.timerEvent)
        elif self.fileSystem.__getitem__("timerEvent") is None or \
                not isinstance(self.fileSystem.__getitem__("timerEvent"), int):
            self.fileSystem.__setitem__("timerEvent", self.timerEvent)
        else:
            self.timerEvent = self.fileSystem.__getitem__("timerEvent")

    def writeClockEvent(self, w: bool = False) -> None:
        """
        Fonction writeClockEvent
        Description:
            Fonction qui permet d'écrire l'heure de l'Event dans le fichier de configuration
        :return: None
        """
        if w:
            self.fileSystem.__setitem__("clockEvent", self.clockEvent.__dict__())
        elif self.fileSystem.__getitem__("clockEvent") is None \
                or not isinstance(self.fileSystem.__getitem__("clockEvent"), dict):
            self.fileSystem.__setitem__("clockEvent", self.clockEvent.__dict__())
        else:
            dictC = self.fileSystem.__getitem__("clockEvent")
            self.clockEvent = Clock(heure=dictC["heure"], minute=dictC["minute"], seconde=dictC["seconde"])

    def writeChanelEvent(self, w: bool = False) -> None:
        """
        Fonction writeChanelEvent
        Description:
            Fonction qui permet d'écrire le channel de l'Event dans le fichier de configuration
        :return: None
        """
        if w:
            self.fileSystem.__setitem__("chanelEvent", self.chanelEvent.id)
        elif self.fileSystem.__getitem__("chanelEvent") is None \
                or not isinstance(self.fileSystem.__getitem__("chanelEvent"), int):
            if self.chanelEvent is not None:
                self.fileSystem.__setitem__("chanelEvent", self.chanelEvent.id)
            else:
                self.fileSystem.__setitem__("chanelEvent", None)
        else:
            self.chanelEvent = self.get_channel(self.fileSystem.__getitem__("chanelEvent"))

    def writeConfig(self, key: str = "all", w: bool = False) -> None:
        """
        Fonction writeConfig
        Description:
            Fonction qui permet d'écrire la configuration du bot dans le fichier config.json
        :return: None
        """
        key = key.lower()

        if key == "all":
            self.writeCommandInit(w)
            self.writeBoolEvent(w)
            self.writeBoolTimeEvent(w)
            self.writeTimerEvent(w)
            self.writeClockEvent(w)
            self.writeChanelEvent(w)
        elif key == "commandinit":
            self.writeCommandInit(w)
        elif key == "boolevent":
            self.writeBoolEvent(w)
        elif key == "booltimeevent":
            self.writeBoolTimeEvent(w)
        elif key == "timerevent":
            self.writeTimerEvent(w)
        elif key == "clockevent":
            self.writeClockEvent(w)
        elif key == "chanelevent":
            self.writeChanelEvent(w)
        else:
            raise Exception("Error: Invalid key")

    def verifConfig(self) -> None:
        """
        Fonction verifFileSystem
        Description:
            Fonction qui permet de vérifier le système de fichier
        :return: None
        """
        if not os.path.exists(self.dataFolder[:-1]):
            os.mkdir(self.dataFolder[:-1])

        if self.fileSystem is None:
            self.fileSystem = JsonFile(path=self.dataFolder + 'config.json')

        for key in self.keys:
            if key not in self.fileSystem.__getAllKey__():
                self.fileSystem.__setitem__(key, None)

        self.writeConfig("all")

    async def isAdmin(self, message: d.Message, commande: bool = False) -> bool:
        """
        Fonction isAdmin
        Description:
            Fonction qui permet de savoir si l'utilisateur est un administrateur
        :param message: d.Message -> Le message reçu
        :param commande: bool -> Booléen qui permet de savoir si la commande est une commande
        :return: bool -> True si l'utilisateur est un administrateur, False sinon
        """
        for role in message.author.roles:
            if role.permissions.administrator:
                if commande:
                    await message.channel.send(message.author.mention + "\nVous êtes administrateur !")
                return True
        await message.channel.send(message.author.mention + "\n Vous n'êtes pas administrateur !")
        return False

    async def logout(self) -> None:
        """
        Fonction logout
        Description:
            Fonction qui permet de déconnecter le bot
        :return: None
        """
        await a.sleep(10)
        print('Logged out')
        exit()

    async def off(self, message: d.Message) -> None:
        """
        Fonction off
        Description:
            Fonction qui permet d'éteindre le bot
        :param message: d.Message -> Le message reçu
        :return: None
        """
        if await self.isAdmin(message=message):
            await message.channel.send('Bye !')
            await self.logout()

    async def setCommandInit(self, message: d.Message) -> None:
        """
        Fonction setCommandInit
        Description:
            Fonction qui permet de changer le caractère d'initialisation des commandes
        :param message: d.Message -> Le message reçu
        :return: None
        """
        if await self.isAdmin(message=message):
            self.CommandInit = message.content.split(' ')[1]
            await message.channel.send("Le caractère d'initialisation des commandes est maintenant : '" +
                                       self.CommandInit + "'")
            self.writeConfig("CommandInit", True)

    async def setChannelEvent(self, message: d.Message) -> None:
        """
        Fonction setChannelEvent
        Description:
            Fonction qui permet de définir le channel dans lequel l'Event est lancé
        :param message: d.Message -> Le message reçu
        :return: None
        """
        if await self.isAdmin(message=message):
            c: t.List[str] = message.content.split(' ')
            if len(c) != 1:
                await message.channel.send('Error: Invalid number of arguments')
            else:
                self.chanelEvent = message.channel
                await message.channel.send('Channel set to ' + message.channel.name)
                await self.chanelEvent.send("This Channel is now in Event Mode")
                self.writeConfig("chanelEvent", True)

    async def startEvent(self, message: d.Message) -> None:
        """
        Fonction startEvent
        Description:
            Fonction qui permet de lancer l'Event
        :param message: d.Message -> Le message reçu
        :return: None
        """
        if await self.isAdmin(message=message):
            c: t.List[str] = message.content.split(' ')
            if len(c) != 2:
                await message.channel.send('Error: Invalid number of arguments')
            elif c[1].lower() not in false + true:
                await message.channel.send('Error: Invalid argument')
            elif c[1].lower() in false:
                self.boolEvent = False
                await message.channel.send('Event stopped')
            elif c[1].lower() in true:
                self.boolEvent = True
                await message.channel.send('Event started')
            self.writeConfig("boolEvent", True)

    async def setTimeEvent(self, message: d.Message) -> None:
        """
        Fonction setTimeEvent
        Description:
            Fonction qui permet de définir l'heure à laquelle l'Event est lancé
        :param message: d.Message -> Le message reçu
        :return: None
        """
        if await self.isAdmin(message=message):
            c: t.List[str] = message.content.split(' ')
            if len(c) != 3:
                await message.channel.send('Error: Invalid number of arguments')
            elif c[1].lower() not in ["hms", "s"]:
                await message.channel.send('Error: Invalid first argument : ' + c[2])
            elif c[1].lower() in ["s"]:
                if c[2].isdigit():
                    self.booltimeEvent = False
                    self.timerEvent = int(c[2])
                    await message.channel.send('Time set to ' + c[2] + 's')
                    self.writeConfig("booltimeEvent", True)
                    self.writeConfig("timerEvent", True)
                else:
                    await message.channel.send('Error: Invalid second argument')
            elif c[1].lower() in ["hms"]:
                heure, minute, seconde = c[2].split(':')
                if heure.isdigit() and minute.isdigit() and seconde.isdigit():
                    self.booltimeEvent = True
                    self.clockEvent = Clock(heure=int(heure), minute=int(minute), seconde=int(seconde))
                    await message.channel.send('Time set to ' + self.clockEvent.__str__())
                    self.writeConfig("booltimeEvent", True)
                    self.writeConfig("clockEvent", True)
                else:
                    await message.channel.send('Error: Invalid second argument')
            else:
                await message.channel.send('Error: Invalid sequence of arguments')

    async def seeConfig(self, message: d.Message) -> None:
        """
        Fonction seeConfig
        Description:
            Fonction qui permet de voir la configuration du bot
        :param message: d.Message -> Le message reçu
        :return: None
        """
        localConfig: dict = {
            "CommandInit": self.CommandInit,
            "boolEvent": self.boolEvent,
            "booltimeEvent": self.booltimeEvent,
            "chanelEvent": self.chanelEvent,
            "clockEvent": self.clockEvent,
            "timerEvent": self.timerEvent
        }
        globalConfig: dict = self.fileSystem.__dict__()
        if await self.isAdmin(message=message):
            c: list = message.content.split(' ')
            if len(c) >= 1:
                if len(c) == 1:
                    c.append("all")
                if c[1].lower() not in self.keys + ["all"]:
                    await message.channel.send('Error: Invalid argument')
                elif len(c) > 3:
                    await message.channel.send('Error: Invalid number of arguments')
                else:
                    if len(c) == 3:
                        if c[2].lower() not in ['local', 'global']:
                            await message.channel.send('Error: Invalid argument')
                    else:
                        c.append('local')
                    msg = ""
                    config = localConfig if len(c) == 2 or c[2].lower() == 'local' else globalConfig
                    for i in config.keys():
                        if c[1].lower() in [i, "all"]:
                            msg += i + " : " + str(config[i]) + "\n"
                    await message.channel.send(msg[:-1])
            else:
                await message.channel.send('Error: Invalid number of arguments')
