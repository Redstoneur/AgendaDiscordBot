# Documentation_BaseDeDonnee

## Description

Ce document décrit comment utiliser la classe python `BaseDeDonnee` pour accéder à une base de données.

```python
import typing
import psycopg2 as psycopg2
from typing import List


########################################################################################################################
######################################## Class BaseDeDonnee ############################################################
########################################################################################################################


class BaseDeDonnee:
    """
    Class BaseDeDonnee
    Description :
        Cette classe permet de gérer les bases de données.
    Attributes :
        NameUser : str
            Le nom d'utilisateur de la base de données.
        Password : str
            Le mot de passe de la base de données.
        NameBase : str
            Le nom de la base de données.
        Host : str
            L'hôte de la base de données.
        Port : str
            Le port de la base de données.
    """
    NameUser: str
    Password: str
    NameBase: str
    Host: str
    Port: str
    
    connection: typing.Any = None
    cursor: typing.Any = None

    def __init__(self, NameUser: str, Password: str, NameBase: str, Host: str, Port: str, initFilePath:str = None) -> None:
        self.NameUser = NameUser
        self.Password = Password
        self.NameBase = NameBase
        self.Host = Host
        self.Port = Port
        if not initFilePath is None:
            self.execute_sqlFile(initFilePath)

    def execute_sqlFile(self, path: str) -> None:
        """
        Method execute_sqlFile
        Description :
            Cette méthode permet d'exécuter un fichier sql.
        :param path: str -> Le chemin vers le fichier sql.
        :return: None
        """
        # connection à la base de données
        connection = psycopg2.connect(user=self.NameUser, password=self.Password, host=self.Host, port=self.Port,
                                      database=self.NameBase)
        cursor = connection.cursor()
        # exécution du fichier sql
        with open(path, 'r') as file:
            cursor.execute(file.read())
        # fermeture de la connexion
        connection.commit()
        cursor.close()
        connection.close()
    
    def execute(self, sql: str) -> None:
        """
        Method execute
        Description :
            Cette méthode permet d'exécuter une requête sql.
        :param sql: str -> La requête sql.
        :return: None
        """
        # connection à la base de données
        connection = psycopg2.connect(user=self.NameUser, password=self.Password, host=self.Host, port=self.Port,
                                      database=self.NameBase)
        cursor = connection.cursor()
        # exécution de la requête sql
        cursor.execute(sql)
        # fermeture de la connexion
        connection.commit()
        cursor.close()
        connection.close()
        
    def execute_return(self, sql: str) -> list:
        """
        Method execute_return
        Description :
            Cette méthode permet d'exécuter une requête sql et de retourner le résultat.
        :param sql: str -> La requête sql.
        :return: list -> Le résultat de la requête sql.
        """
        # connection à la base de données
        connection = psycopg2.connect(user=self.NameUser, password=self.Password, host=self.Host, port=self.Port,
                                      database=self.NameBase)
        cursor = connection.cursor()
        # exécution de la requête sql
        cursor.execute(sql)
        # fermeture de la connexion
        connection.commit()
        cursor.close()
        connection.close()
        # retour du résultat
        return cursor.fetchall()
    
    def execute_select(self, toSelect: List[dict], fromTable: List[str], join: List[dict] = None, where: List[dict] = None,
                       groupBy: List[str] = None, having: List[dict] = None, orderBy: List[dict] = None) -> list:
        """
        Method execute_select
        Description :
            Cette méthode permet d'exécuter une requête sql de type select et de retourner le résultat.
        :param toSelect: List[dict] -> Les éléments à sélectionner.
        :param fromTable: List[str] -> Les tables à sélectionner.
        :param join: List[dict] -> Les jointures à faire.
        :param where: List[dict] -> Les conditions à appliquer.
        :param groupBy: List[str] -> Les groupements à appliquer.
        :param having: List[dict] -> Les conditions à appliquer après le groupement.
        :param orderBy: List[dict] -> Les ordonnancements à appliquer.
        :return: list -> Le résultat de la requête sql.
        """
        # construction de la requête sql
        sql = "SELECT "
        for i in range(len(toSelect)):
            sql += toSelect[i]["name"]
            if "alias" in toSelect[i]:
                sql += " AS " + toSelect[i]["alias"]
            if i < len(toSelect) - 1:
                sql += ", "
        sql += " FROM "
        for i in range(len(fromTable)):
            sql += fromTable[i]
            if i < len(fromTable) - 1:
                sql += ", "
        if not join is None:
            for i in range(len(join)):
                sql += " " + join[i]["type"] + " JOIN " + join[i]["table"] + " ON " + join[i]["condition"]
        if not where is None:
            sql += " WHERE "
            for i in range(len(where)):
                sql += where[i]["name"] + " " + where[i]["operator"] + " " + where[i]["value"]
                if i < len(where) - 1:
                    sql += " AND "
        if not groupBy is None:
            sql += " GROUP BY "
            for i in range(len(groupBy)):
                sql += groupBy[i]
                if i < len(groupBy) - 1:
                    sql += ", "
        if not having is None:
            sql += " HAVING "
            for i in range(len(having)):
                sql += having[i]["name"] + " " + having[i]["operator"] + " " + having[i]["value"]
                if i < len(having) - 1:
                    sql += " AND "
        if not orderBy is None:
            sql += " ORDER BY "
            for i in range(len(orderBy)):
                sql += orderBy[i]["name"] + " " + orderBy[i]["order"]
                if i < len(orderBy) - 1:
                    sql += ", "
        # exécution de la requête sql
        return self.execute_return(sql)
    
    def execute_insert(self, intoTable: str, values: List[dict]) -> None:
        """
        Method execute_insert
        Description :
            Cette méthode permet d'exécuter une requête sql de type insert.
        :param intoTable: str -> La table dans laquelle insérer.
        :param values: List[dict] -> Les valeurs à insérer.
        :return: None
        """
        # construction de la requête sql
        sql = "INSERT INTO " + intoTable + " ("
        for i in range(len(values)):
            sql += values[i]["name"]
            if i < len(values) - 1:
                sql += ", "
        sql += ") VALUES ("
        for i in range(len(values)):
            sql += values[i]["value"]
            if i < len(values) - 1:
                sql += ", "
        sql += ")"
        # exécution de la requête sql
        self.execute(sql)
        
    def execute_update(self, table: str, set: List[dict], where: List[dict]) -> None:
        """
        Method execute_update
        Description :
            Cette méthode permet d'exécuter une requête sql de type update.
        :param table: str -> La table à modifier.
        :param set: List[dict] -> Les valeurs à modifier.
        :param where: List[dict] -> Les conditions à appliquer.
        :return: None
        """
        # construction de la requête sql
        sql = "UPDATE " + table + " SET "
        for i in range(len(set)):
            sql += set[i]["name"] + " = " + set[i]["value"]
            if i < len(set) - 1:
                sql += ", "
        sql += " WHERE "
        for i in range(len(where)):
            sql += where[i]["name"] + " " + where[i]["operator"] + " " + where[i]["value"]
            if i < len(where) - 1:
                sql += " AND "
        # exécution de la requête sql
        self.execute(sql)
        
    def execute_delete(self, fromTable: str, where: List[dict]) -> None:
        """
        Method execute_delete
        Description :
            Cette méthode permet d'exécuter une requête sql de type delete.
        :param fromTable: str -> La table à modifier.
        :param where: List[dict] -> Les conditions à appliquer.
        :return: None
        """
        # construction de la requête sql
        sql = "DELETE FROM " + fromTable + " WHERE "
        for i in range(len(where)):
            sql += where[i]["name"] + " " + where[i]["operator"] + " " + where[i]["value"]
            if i < len(where) - 1:
                sql += " AND "
        # exécution de la requête sql
        self.execute(sql)
```

## Utilisation

### Création d'une base de données

Pour créer une base de données, il suffit d'instancier la classe `BaseDeDonnee` avec le chemin vers le fichier de la base de données.

```python
from generique.BaseDeDonnee import BaseDeDonnee

bdd = BaseDeDonnee(
                    NameUser='NomUtilisateur',
                    Password='MotDePasse',
                    Host='AdresseServeur',
                    Port='PortServeur',
                    NameBase='NomBaseDeDonnees',
                    initFilePath='chemin/vers/le/fichier/init.sql'
                )
```

### Exécution d'une requête

Pour exécuter une requête sans récupérer de résultat, il suffit d'utiliser la méthode `execute` de la classe `BaseDeDonnee`.

```python
bdd.execute('SELECT * FROM table')
```

Pour exécuter une requête en récupérant des résultats, il suffit d'utiliser la méthode `execute_return` de la classe `BaseDeDonnee`.

```python
result = bdd.execute_return('SELECT * FROM table')
```

### Exécution d'un Script SQL

Pour exécuter un script SQL, il suffit d'utiliser la méthode `execute_sqlFile` de la classe `BaseDeDonnee`.

```python
bdd.execute_sqlFile()
```

### Exécution d'un SELECT

Pour exécuter un SELECT, il suffit d'utiliser la méthode `execute_select` de la classe `BaseDeDonnee`.

```python
result = bdd.select(toSelect=[{
                                "name": "NomColonne",
                                "alias": "AliasColonne"
                                }],
                    fromTable="NomTable",
                    where=[{
                            "name": "NomColonne",
                            "operator": "Operateur",
                            "value": "Valeur"
                            }],
                    groupBy=["NomColonne"],
                    having=[{
                            "name": "NomColonne",
                            "operator": "Operateur",
                            "value": "Valeur"
                            }],
                    orderBy=[{
                            "name": "NomColonne",
                            "order": "ASC/DESC"
                            }]
                    )

```

La variable `toSelect` est une liste de dictionnaires contenant les noms des colonnes à sélectionner et leurs alias.
```txt
[
    {
        "name": "NomDeColonne",
        "alias": "AliasDeColonne"
    }
]
```

La variable `fromTable` est une chaîne de caractères contenant le nom de la table à sélectionner.
```txt
"NomDeTable"
```


