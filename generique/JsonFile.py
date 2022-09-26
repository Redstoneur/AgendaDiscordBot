import json
import os
import typing as t

########################################################################################################################
######################################## Class JsonFile ################################################################
########################################################################################################################


class JsonFile:
    """
    Class JsonFile
    Description:
        Cette classe permet de gérer les fichiers json.
    Attributes:
        path: str
            Le chemin vers le fichier json.
        data: dict
            Les données du fichier json.
    """
    path: str = None
    data: dict = None

    def __init__(self, path: str):
        """
        Constructeur de la classe JsonFile.
        :param path: str -> Le chemin vers le fichier json.
        """
        self.path = path
        if os.path.exists(path):
            self.read()
        else:
            self.data = {}
            self.create()

    def read(self) -> None:
        """
        Method read
        Description:
            Cette méthode permet de lire le fichier json.
        :return: None
        """
        try:
            with open(self.path, 'r') as file:
                self.data = json.load(file)
        except json.decoder.JSONDecodeError:
            self.data = {}

    def write(self) -> None:
        """
        Method write
        Description:
            Cette méthode permet d'écrire dans le fichier json.
        :return: None
        """
        try:
            with open(self.path, 'w') as file:
                json.dump(self.data, file)
        except TypeError:
            pass

    def create(self) -> None:
        """
        Method create
        Description:
            Cette méthode permet de créer le fichier json vide.
        :return: None
        """
        try:
            with open(self.path, 'w') as file:
                file.write('{}')
        except TypeError:
            pass

    def __str__(self) -> str:
        """
        Method __str__
        Description:
            Cette méthode permet de retourner une chaîne de caractères représentant l'objet JsonFile.
        :return: str
        """
        return str(self.data)

    def __dict__(self) -> dict:
        """
        Method __dict__
        Description:
            Cette méthode permet de retourner un dictionnaire représentant l'objet JsonFile.
        :return: dict
        """
        return self.data

    def __getAllKey__(self) -> t.List[str]:
        """
        Method __getKey__
        Description:
            Cette méthode permet de retourner la liste des clés du fichier json.
        :return: List[str]
        """
        return list(self.data.keys())

    def __addkey__(self,key: str) -> None:
        """
        Method __addkey__
        Description:
            Cette méthode permet d'ajouter un attribut à la classe JsonFile.
        :param key: str -> La clé de l'attribut.
        :return: None
        """
        self.__setitem__(key, None)
        self.write()

    def __getitem__(self, key: str) -> t.Any:
        """
        Method __getitem__
        Description:
            Cette méthode permet de retourner la valeur d'un attribut de la classe JsonFile.
        :param key: str -> La clé de l'attribut.
        :return: t.Any
        """
        try:
            return self.data[key]
        except KeyError:
            raise KeyError("The key '{}' does not exist.".format(key))

    def __setitem__(self, key: str, value: t.Any) -> None:
        """
        Method __setitem__
        Description:
            Cette méthode permet de modifier la valeur d'un attribut de la classe JsonFile.
        :param key: str -> La clé de l'attribut.
        :param value: t.Any -> La valeur de l'attribut.
        :return: None
        """
        self.data[key] = value
        self.write()

    def __delitem__(self, key: str) -> None:
        """
        Method __delitem__
        Description:
            Cette méthode permet de supprimer un attribut de la classe JsonFile.
        :param key: str -> La clé de l'attribut.
        :return: None
        """
        del self.data[key]
        self.write()

    def __contains__(self, key: str) -> bool:
        """
        Method __contains__
        Description:
            Cette méthode permet de vérifier si un attribut existe dans la classe JsonFile.
        :param key: str -> La clé de l'attribut.
        :return: bool
        """
        return key in self.data

    def __iter__(self) -> t.Iterator:
        """
        Method __iter__
        Description:
            Cette méthode permet d'itérer sur les attributs de la classe JsonFile.
        :return: t.Iterator
        """
        return iter(self.data)

    def __len__(self) -> int:
        """
        Method __len__
        Description:
            Cette méthode permet de retourner le nombre d'attributs de la classe JsonFile.
        :return: int
        """
        return len(self.data)


