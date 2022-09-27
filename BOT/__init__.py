from BOT.Bot import *


def main(url: str = None, Token: str = None) -> None:
    """
    Main function of the BOT
    :param url: url of the pdf file
    :param Token: token of the bot
    :return: None
    """

    # vérification get token
    if Token is None:
        try:
            Token: str = os.environ['TOKEN']
        except KeyError:
            raise KeyError('TOKEN not found')
    else:
        print('Token set')

    # vérification de l'url
    if url is None:
        try:
            url: str = os.environ['URL']
        except KeyError:
            raise KeyError('URL not found')
    else:
        print('Url set')

    # intents de connexion
    intents = d.Intents.default()  # default, all but presences and member caching
    intents.message_content = True  # permet de récupérer le contenu des messages
    # intents = d.Intents.all()  # pour tout les intents

    # vider le terminal
    clearTerminal()

    # création du bot
    bot = Bot(url=url, intents=intents)

    # connexion au bot
    bot.run(Token)
