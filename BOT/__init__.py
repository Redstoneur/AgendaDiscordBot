from BOT.Bot import *


def main(url: str, Token: str = None):
    # vérification get token
    if Token is None:
        try:
            Token: str = os.environ['TOKEN']
        except KeyError:
            raise KeyError('TOKEN not found')

    # vérification du token
    if Token is None:
        raise ValueError('Token not set')
    else:
        print('Token set')

    # vérification de l'url
    if url is None:
        raise ValueError('Url not set')
    else:
        print('Url set')

    # intents de connexion
    # intents = d.Intents.default()
    # intents.message_content = True
    intents = d.Intents.all()

    # création du bot
    bot = Bot(url=url, intents=intents)

    # connexion au bot
    bot.run(Token)
