from Clock import *
from TimeTable import TimeTable
from importBot import t, d, a, os

false: t.List[str] = ['false', 'f', 'no', 'n', '0']
true: t.List[str] = ['true', 't', 'yes', 'y', '1']


class Bot(d.Client):
    CommandInit: str = '!'
    boolEvent: bool = False
    timerEvent: int = 10  # 3600
    clockEvent: Clock = Clock(heure=8, minute=0, seconde=0)
    booltimeEvent: bool = False
    chanelEvent: d.TextChannel = None
    timetable: TimeTable

    def __init__(self, url: str, *args, **kwargs):
        self.timetable = TimeTable(url=url)
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('Logged in as {0.user}'.format(self))
        await self.Event()

    async def on_message(self, message: d.Message):
        if message.author == self.user:
            return
        if message.content.startswith(self.CommandInit + 'hello'):
            await message.channel.send('Hello ' + message.author.name + ' !')

        elif message.content.startswith('ping'):
            await message.channel.send('pong')

        elif message.content.endswith('quoi'):
            await message.channel.send('feur')

        elif message.content.startswith(self.CommandInit + 'off'):
            if message.author.roles[-1].permissions.administrator:
                await message.channel.send('Bye!')
                await self.logout()
            else:
                await message.channel.send('You are not an administrator')

        elif message.content.startswith(self.CommandInit + 'setCommandInit'):
            self.CommandInit = message.content.split(' ')[1]
            await message.channel.send('CommandInit set to ' + self.CommandInit)

        elif message.content.startswith(self.CommandInit + 'startEvent'):
            await self.startEvent(message)

        elif message.content.startswith(self.CommandInit + 'setChannelEvent'):
            await self.setChannelEvent(message)

        elif message.content.startswith(self.CommandInit + 'setTimeEvent'):
            await self.setTimeEvent(message)

    async def Event(self):
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
                    await self.chanelEvent.send('@Redstoneur Emplois du temps :')
                    await self.chanelEvent.send(file=d.File('file.png'))
                elif os.path.exists('file.pdf'):
                    await self.chanelEvent.send(file=d.File('file.pdf'))
                else:
                    await self.chanelEvent.send('Emplois du temps')

    async def logout(self):
        await super().close()
        await a.sleep(10)
        print('Logged out')
        exit(0)

    async def setChannelEvent(self, message: d.Message):
        c: t.List[str] = message.content.split(' ')
        if len(c) != 1:
            await message.channel.send('Error: Invalid number of arguments')
        else:
            self.chanelEvent = message.channel
            await message.channel.send('Channel set to ' + message.channel.name)
            await self.chanelEvent.send("This Channel is now in Event Mode")

    async def startEvent(self, message: d.Message):
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

    async def setTimeEvent(self, message: d.Message):
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



