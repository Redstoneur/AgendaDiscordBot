from importBot import t, d, a

false: t.List[str] = ['false', 'f', 'no', 'n', '0']
true: t.List[str] = ['true', 't', 'yes', 'y', '1']


class Bot(d.Client):
    CommandInit: str = '!'
    boolEvent: bool = False
    timerEvent: int = 10  # 3600
    chanelEvent: d.TextChannel = None

    def __init__(self, *args, **kwargs):
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
            await message.channel.send('Bye!')
            await self.logout()

        elif message.content.startswith(self.CommandInit + 'setCommandInit'):
            self.CommandInit = message.content.split(' ')[1]
            await message.channel.send('CommandInit set to ' + self.CommandInit)

        elif message.content.startswith(self.CommandInit + 'setTimerEvent'):
            await self.setTimerEvent(message)

        elif message.content.startswith(self.CommandInit + 'startEvent'):
            await self.startEvent(message)

        elif message.content.startswith(self.CommandInit + 'setChannelEvent'):
            await self.setChannelEvent(message)

    async def Event(self):
        await self.chanelEvent.send("This Channel is now in Event Mode")
        while not self.is_closed():
            if self.boolEvent and self.chanelEvent is not None:
                await self.chanelEvent.send('Emplois du temps')
            await a.sleep(self.timerEvent)

    async def logout(self):
        await super().close()
        await a.sleep(10)
        print('Logged out')
        exit(0)

    async def setTimerEvent(self, message: d.Message):
        c: t.List[str] = message.content.split(' ')
        if len(c) != 2:
            await message.channel.send('Error: Invalid number of arguments')
        elif not c[1].isdigit():
            await message.channel.send('Error: Invalid argument')
        else:
            self.timerEvent = int(c[1])
            await message.channel.send('Timer set to ' + c[1])

    async def setChannelEvent(self, message: d.Message):
        c: t.List[str] = message.content.split(' ')
        if len(c) != 1:
            await message.channel.send('Error: Invalid number of arguments')
        else:
            self.chanelEvent = message.channel
            await message.channel.send('Channel set to ' + message.channel.name)

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
