from generique.JsonFile import JsonFile
import os


def myOS() -> str:
    """
    Fonction myOS
    Description :
        Cette fonction permet de définir le système d'exploitation.
    :return: str -> OS
    """
    # windows
    if os.name == 'nt':
        return 'Windows'
    # linux ubuntu
    elif os.name == 'posix':
        return 'Linux'
    # mac
    elif os.name == 'mac':
        return 'Mac'
    # unknown
    else:
        return 'Unknown'


def clearTerminal() -> None:
    """
    Fonction clearTerminal
    Description :
        Cette fonction permet de nettoyer le terminal.
    :return: None
    """
    if myOS() == 'Windows':
        os.system('cls')
    elif myOS() in ['Linux', 'Mac']:
        os.system('clear')
    else:
        print("\n" * 100)
