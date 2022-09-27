from BOT.importBot import t, dt


########################################################################################################################
######################################## Class Clock ###################################################################
########################################################################################################################

class Clock:
    """
    Class Clock
    Description:
        Cette classe permet de gérer les horaires.
    Attributs:
        heure: int
            L'heure de l'horloge.
        minute: int
            Les minutes de l'horloge.
        seconde: int
            Les secondes de l'horloge.
    """

    heure: int = 0
    minute: int = 0
    seconde: int = 0

    def __init__(self, heure: int, minute: int, seconde: int = 0) -> None:
        """
        Constructeur de la classe Clock.
        :param heure: int -> L'heure de l'horloge.
        :param minute: int -> Les minutes de l'horloge.
        :param seconde: int -> Les secondes de l'horloge.
        """
        self.heure = heure
        self.minute = minute
        self.seconde = seconde
        self.__verif__()

    def __verif__(self) -> None:
        """
        Méthode __verif__
        Description:
            Cette méthode permet de vérifier les attributs de la classe Clock.
        :return: None
        """
        if self.seconde >= 60:
            self.seconde -= 60
            self.minute += 1
        if self.minute >= 60:
            self.minute -= 60
            self.heure += 1
        if self.heure >= 24:
            self.heure -= 24

    def __str__(self) -> str:
        """
        Méthode __str__
        Description:
            Cette méthode permet de retourner une chaîne de caractères représentant l'objet Clock.
        :return: str
        """
        return str(self.heure) + ':' + str(self.minute) + ':' + str(self.seconde)

    def __getinitargs__(self) -> t.Tuple[int, int, int]:
        """
        Méthode __getinitargs__
        Description:
            Cette méthode permet de retourner un tuple contenant les arguments du constructeur de la classe Clock.
        :return: t.Tuple[int, int, int]
        """
        return self.heure, self.minute, self.seconde

    def __dict__(self) -> t.Dict[str, int]:
        """
        Méthode __dict__
        Description:
            Cette méthode permet de retourner un dictionnaire contenant les attributs de la classe Clock.
        :return: t.Dict[str, int]
        """
        return {'heure': self.heure, 'minute': self.minute, 'seconde': self.seconde}

    def __getitem__(self, key) -> int:
        """
        Méthode __getitem__
        Description:
            Cette méthode permet de retourner la valeur d'un attribut de la classe Clock.
        :param key: str -> La clé de l'attribut.
        :return: int
        """
        return self.__dict__()[key]

    def __setitem__(self, key, value) -> None:
        """
        Méthode __setitem__
        Description:
            Cette méthode permet de modifier la valeur d'un attribut de la classe Clock.
        :param key: str -> La clé de l'attribut.
        :param value: int -> La valeur de l'attribut.
        :return: None
        """
        self.__dict__()[key] = value

    def __delitem__(self, key) -> None:
        """
        Méthode __delitem__
        Description:
            Cette méthode permet de supprimer un attribut de la classe Clock.
        :param key: str -> La clé de l'attribut.
        :return: None
        """
        del self.__dict__()[key]

    def __getkey__(self) -> t.List[str]:
        """
        Méthode __getkey__
        Description:
            Cette méthode permet de retourner la liste des clés des attributs de la classe Clock.
        :return: t.List[str]
        """
        return list(self.__dict__().keys())

    def __eq__(self, other: 'Clock') -> bool:
        """
        Méthode __eq__
        Description:
            Cette méthode permet de vérifier si deux objets Clock sont égaux.
        :param other: Clock -> L'autre objet Clock.
        :return: bool
        """
        if isinstance(other, Clock):
            return self.heure == other.heure and self.minute == other.minute and self.seconde == other.seconde
        return False

    def __sup__(self, other: 'Clock') -> bool:
        """
        Méthode __sup__
        Description:
            Cette méthode permet de vérifier si un objet Clock est supérieur à un autre objet Clock.
        :param other: Clock -> L'autre objet Clock.
        :return: bool
        """
        if isinstance(other, Clock):
            if self.heure > other.heure:
                return True
            elif self.heure == other.heure:
                if self.minute > other.minute:
                    return True
                elif self.minute == other.minute:
                    if self.seconde > other.seconde:
                        return True
        return False

    def __inf__(self, other: 'Clock') -> bool:
        """
        Méthode __inf__
        Description:
            Cette méthode permet de vérifier si un objet Clock est inférieur à un autre objet Clock.
        :param other: Clock -> L'autre objet Clock.
        :return: bool
        """
        if isinstance(other, Clock):
            if self.heure < other.heure:
                return True
            elif self.heure == other.heure:
                if self.minute < other.minute:
                    return True
                elif self.minute == other.minute:
                    if self.seconde < other.seconde:
                        return True
        return False

    def __center__(self, other: 'Clock', other2: 'Clock') -> bool:
        """
        Méthode __center__
        Description:
            Cette méthode permet de vérifier si un objet Clock est compris entre deux autres objets Clock.
        :param other: Clock -> L'autre objet Clock.
        :param other2: Clock -> L'autre objet Clock.
        :return: bool true si l'objet Clock est compris entre les deux autres objets Clock.
        """
        if isinstance(other, Clock) and isinstance(other2, Clock):
            if self.__sup__(other) and self.__inf__(other2):
                return True
            elif self.__sup__(other2) and self.__inf__(other):
                return True
        return False

    def __add__(self, other: 'Clock') -> None:
        """
        Méthode __add__
        Description:
            Cette méthode permet d'ajouter un objet Clock à un autre objet Clock.
        :param other: Clock -> L'autre objet Clock.
        :return:
        """
        if isinstance(other, Clock):
            self.heure = self.heure + other.heure
            self.minute = self.minute + other.minute
            self.seconde = self.seconde + other.seconde
            self.__verif__()

    def __add2__(self, heure: int = 0, minute: int = 0, seconde: int = 0) -> None:
        self.heure = self.heure + heure
        self.minute = self.minute + minute
        self.seconde = self.seconde + seconde
        self.__verif__()

    def __getPostClock__(self, other: 'Clock') -> 'Clock':
        """
        Méthode __getPostClock__
        Description:
            Cette méthode permet de retourner un objet Clock qui est la somme de deux objets Clock.
        :param other: Clock -> L'autre objet Clock.
        :return: Clock
        """
        if isinstance(other, Clock):
            heure = self.heure + other.heure
            minute = self.minute + other.minute
            seconde = self.seconde + other.seconde
            return Clock(heure, minute, seconde)
        else:
            raise TypeError('other doit être de type Clock')

    def __getPostClock2__(self, heure: int = 0, minute: int = 0, seconde: int = 0) -> 'Clock':
        """
        Méthode __getPostClock2__
        Description:
            Cette méthode permet de retourner un objet Clock qui est la somme de deux objets Clock.
        :param heure: int -> L'heure de l'objet Clock.
        :param minute: int -> La minute de l'objet Clock.
        :param seconde: int -> La seconde de l'objet Clock.
        :return: Clock
        """
        if isinstance(heure, int) and isinstance(minute, int) and isinstance(seconde, int):
            heure = self.heure + heure
            minute = self.minute + minute
            seconde = self.seconde + seconde
            return Clock(heure, minute, seconde)
        else:
            raise TypeError('heure, minute et seconde doivent être de type int')


def whatTimeIsIt() -> Clock:
    """
    Fonction whatTimeIsIt
    Description:
        Cette fonction permet de retourner l'heure actuelle.
    :return: Clock
    """
    now: dt.datetime = dt.datetime.now()
    return Clock(now.hour, now.minute, now.second)
