from Bot import *

token: str = os.environ['TOKEN']

if token is None:
    raise ValueError('Token not set')
else:
    print('Token set')

intents = d.Intents.default()
intents.message_content = True

if __name__ == "__main__":
    client: Bot = Bot(url="http://chronos.iut-velizy.uvsq.fr/EDT/g37478.pdf",
                      intents=intents)
    client.run(token)
