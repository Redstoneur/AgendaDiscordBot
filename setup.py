import os

import discord as d

token: str = os.environ['TOKEN']
if token is None:
    raise ValueError('Token not set')
else:
    print('Token set')

intents = d.Intents.default()
intents.message_content = True

client: d.Client = d.Client(intents=intents)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message: d.Message):
    if message.author == client.user:
        return
    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')


client.run(token)
