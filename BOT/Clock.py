from BOT.importBot import t, dt


class Clock:
    heure: int = 0
    minute: int = 0
    seconde: int = 0

    def __init__(self, heure: int, minute: int, seconde: int = 0) -> None:
        self.heure = heure
        self.minute = minute
        self.seconde = seconde
        self.__verif__()

    def __verif__(self) -> None:
        if self.seconde >= 60:
            self.seconde -= 60
            self.minute += 1
        if self.minute >= 60:
            self.minute -= 60
            self.heure += 1
        if self.heure >= 24:
            self.heure -= 24

    def __str__(self) -> str:
        return str(self.heure) + ':' + str(self.minute) + ':' + str(self.seconde)

    def __getinitargs__(self) -> t.Tuple[int, int, int]:
        return self.heure, self.minute, self.seconde

    def __dict__(self) -> t.Dict[str, int]:
        return {'heure': self.heure, 'minute': self.minute, 'seconde': self.seconde}

    def __getitem__(self, key) -> int:
        return self.__dict__()[key]

    def __setitem__(self, key, value) -> None:
        self.__dict__()[key] = value

    def __delitem__(self, key) -> None:
        del self.__dict__()[key]

    def __getkey__(self) -> t.List[str]:
        return list(self.__dict__().keys())

    def __eq__(self, other: 'Clock') -> bool:
        if isinstance(other, Clock):
            return self.heure == other.heure and self.minute == other.minute and self.seconde == other.seconde
        return False

    def __sup__(self, other: 'Clock') -> bool:
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

    def __add__(self, other: 'Clock') -> None:
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


def whatTimeIsIt() -> Clock:
    now: dt.datetime = dt.datetime.now()
    return Clock(now.hour, now.minute, now.second)


if __name__ == '__main__':
    clock: Clock = whatTimeIsIt()
    clock.__add2__(seconde=10)
    print("finale clock: " + clock.__str__())
    localtime: Clock = whatTimeIsIt()
    while clock.__inf__(whatTimeIsIt()) is False:
        print(whatTimeIsIt().__str__() + " != " + clock.__str__())
        localtime: Clock = whatTimeIsIt()
