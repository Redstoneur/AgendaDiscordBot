import mysql.connector
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

    def __init__(self, NameUser: str, Password: str, NameBase: str, Host: str, Port: str,
                 initFilePath: str = None) -> None:
        self.NameUser = NameUser
        self.Password = Password
        self.NameBase = NameBase
        self.Host = Host
        self.Port = Port
        if initFilePath is not None:
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
        connection = mysql.connector.connect(
            host=self.Host,
            user=self.NameUser,
            password=self.Password,
            database=self.NameBase,
            port=self.Port
        )
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
        connection = mysql.connector.connect(
            host=self.Host,
            user=self.NameUser,
            password=self.Password,
            database=self.NameBase,
            port=self.Port
        )
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
        connection = mysql.connector.connect(
            host=self.Host,
            user=self.NameUser,
            password=self.Password,
            database=self.NameBase,
            port=self.Port
        )
        cursor = connection.cursor()
        # exécution de la requête sql
        cursor.execute(sql)
        # fermeture de la connexion
        connection.commit()
        cursor.close()
        connection.close()
        # retour du résultat
        return cursor.fetchall()

    def execute_select(self, toSelect: List[dict], fromTable: List[str], join: List[dict] = None,
                       where: List[dict] = None,
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
        if join is not None:
            for i in range(len(join)):
                sql += " " + join[i]["type"] + " JOIN " + join[i]["table"] + " ON " + join[i]["condition"]
        if where is not None:
            sql += " WHERE "
            for i in range(len(where)):
                sql += where[i]["name"] + " " + where[i]["operator"] + " " + where[i]["value"]
                if i < len(where) - 1:
                    sql += " AND "
        if groupBy is not None:
            sql += " GROUP BY "
            for i in range(len(groupBy)):
                sql += groupBy[i]
                if i < len(groupBy) - 1:
                    sql += ", "
        if having is not None:
            sql += " HAVING "
            for i in range(len(having)):
                sql += having[i]["name"] + " " + having[i]["operator"] + " " + having[i]["value"]
                if i < len(having) - 1:
                    sql += " AND "
        if orderBy is not None:
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
