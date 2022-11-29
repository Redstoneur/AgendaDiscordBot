from BOT.Bot import *


def main(url: str = None, Token: str = None) -> None:
    """
    Main function of the BOT
    :param url: url of the pdf file
    :param Token: token of the bot
    :return: None
    """

    NameUser: str
    Password: str
    NameBase: str
    Host: str
    Port: str

    # Nom de l'utilisateur de la base de données.
    try:
        NameUser: str = os.environ['DB_USER']
    except KeyError:
        raise KeyError('NameUser not found in the environment variables')

    # Mot de passe de l'utilisateur de la base de données.
    try:
        Password: str = os.environ['DB_PASSWORD']
    except KeyError:
        raise KeyError('Password not found in the environment variables')

    # Nom de la base de données.
    try:
        NameBase: str = os.environ['DB_NAME']
    except KeyError:
        raise KeyError('NameBase not found in the environment variables')

    # Hôte de la base de données.
    try:
        Host: str = os.environ['DB_HOST']
    except KeyError:
        raise KeyError('Host not found in the environment variables')

    # Port de la base de données.
    try:
        Port: str = os.environ['DB_PORT']
    except KeyError:
        raise KeyError('Port not found in the environment variables')

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
    print('\nStarting bot...')

    # création du bot
    bot = Bot(NameUser=NameUser,
              Password=Password,
              NameBase=NameBase,
              Host=Host,
              Port=Port,
              url=url,
              intents=intents
              )

    # connexion au bot
    bot.run(Token)
