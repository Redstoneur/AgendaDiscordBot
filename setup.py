import os

import discord as d

token = os.environ.get("TOKEN")
print(token)
token=os.environ['TOKEN']
print(token)

class MyClient(d.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hello'):
            await message.channel.send('Hello {0.author.mention}'.format(message))


intents = d.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token=os.environ['TOKEN'])
