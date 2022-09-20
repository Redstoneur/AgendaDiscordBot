from importBot import os
from Bot import *

token: str = os.environ['TOKEN']

if token is None:
    raise ValueError('Token not set')
else:
    print('Token set')

intents = d.Intents.default()
intents.message_content = True

client: Bot = Bot(intents=intents)
client.run(token)
