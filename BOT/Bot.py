from BOT.Clock import *
from BOT.TimeTable import TimeTable
from BOT.importBot import t, d, a, os

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
        CommandInit: str
            Le caractère qui permet d'initialiser une commande
        boolEvent: bool
            Booléen qui permet de savoir si l'Event est activé ou non
        booltimeEvent: bool
            Booléen qui permet de savoir le type de timerEvent
        chanelEvent: d.Channel
            Le channel dans lequel l'Event est lancé
        clockEvent: Clock
            L'heure à laquelle l'Event est lancé
        timerEvent: int
            Le temps en secondes entre chaque lancement de l'Event
        timetable: TimeTable
            L'emploi du temps
    """
    CommandInit: str = '!'
    boolEvent: bool = False
    timerEvent: int = 10  # 3600
    clockEvent: Clock = Clock(heure=8, minute=0, seconde=0)
    booltimeEvent: bool = False
    chanelEvent: d.TextChannel = None
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
        self.timetable = TimeTable(url=url)
        super().__init__(*args, **kwargs)

    async def on_ready(self) -> None:
        """
        Fonction on_ready
        Description:
            Fonction qui est appelée lorsque le bot est prêt
        :return: None
        """
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
                    await self.chanelEvent.send(file=d.File('../TimeTable.pdf'))
                elif os.path.exists('../file.pdf'):
                    await self.chanelEvent.send('Emplois du temps :')
                    await self.chanelEvent.send(file=d.File('../file.pdf'))
                else:
                    await self.chanelEvent.send('Emplois du temps')

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
                else:
                    await message.channel.send('Error: Invalid second argument')
            elif c[1].lower() in ["hms"]:
                heure, minute, seconde = c[2].split(':')
                if heure.isdigit() and minute.isdigit() and seconde.isdigit():
                    self.booltimeEvent = True
                    self.clockEvent = Clock(heure=int(heure), minute=int(minute), seconde=int(seconde))
                    await message.channel.send('Time set to ' + self.clockEvent.__str__())
                else:
                    await message.channel.send('Error: Invalid second argument')
            else:
                await message.channel.send('Error: Invalid sequence of arguments')
