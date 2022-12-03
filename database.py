import mysql.connector
import config
from datetime import datetime


class DBClient:
    def __init__(self, db_host, db_username, db_password):
        self.client = mysql.connector.connect(host=db_host,
                                              user=db_username,
                                              password=db_password,
                                              database="pydiscordbot")

    def executeSQL(self, sql, query=True):
        mycursor = self.client.cursor()
        mycursor.execute(sql)
        if query != True:
            self.client.commit()
        myresult = mycursor.fetchall()
        return myresult

    def getUsers(self):
        sql = "SELECT * FROM users"
        return self.executeSQL(sql)

    def getUserInfo(self, DiscordID):
        sql = 'SELECT * FROM users WHERE DISCORDID = {}'.format(DiscordID)
        return self.executeSQL(sql)[0]

    def adduser(self, DiscordID, DiscordName):
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO `users` VALUES ('{0}','{1}','0','{2}','NULL');".format(DiscordID, DiscordName, dt_string)
        self.executeSQL(sql, False)

    def setBirthday(self, DiscordID, birthday):
        sql = "UPDATE `users` SET `Birthday` = '{0}' WHERE DISCORDID = '{1}'".format(birthday, DiscordID)
        self.executeSQL(sql, False)

    def updateBalance(self, DiscordID, value: int, option=""):
        balance = 0;
        if option == "set":
            balance = value;
            sql = "UPDATE `users` SET `Balance` = {0} WHERE DISCORDID = {1}".format(value, DiscordID)
        else:
            sql = "SELECT Balance FROM users WHERE DISCORDID = {0}".format(DiscordID)
            balance = self.getBalance(DiscordID)
            balance = balance + value
            sql = "UPDATE `users` SET `Balance` = {0} WHERE DISCORDID = {1}".format(balance, DiscordID)
            self.executeSQL(sql, False)

    def getBalance(self, DiscordID):
        sql = "SELECT Balance FROM users WHERE DISCORDID = {0}".format(DiscordID)
        return self.executeSQL(sql)[0][0]
