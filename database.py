import mysql.connector
import config
from datetime import datetime


class Database:
    def __init__(self, db_host, db_username, db_password,db_name):
        print("Connecting to MySQL server...")
        self.client = mysql.connector.connect(host=db_host,
                                              user=db_username,
                                              password=db_password,
                                              database=db_name)

    def executeSQL(self, sql, query=True):
        mycursor = self.client.cursor()
        mycursor.execute(sql)
        if query != True:
            self.client.commit()
        myresult = mycursor.fetchall()
        return myresult

    def getUsers(self):
        sql = "SELECT * FROM master"
        return self.executeSQL(sql)

    def getUserInfo(self, DiscordID):
        sql = 'SELECT * FROM master WHERE DISCORDID = {}'.format(DiscordID)
        return self.executeSQL(sql)[0]

    def adduser(self, DiscordID, DiscordName):
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        sql = "INSERT INTO `master` VALUES ('{0}','{1}','0','0','{2}','NULL');".format(DiscordID,DiscordName,dt_string)
        try:
            self.executeSQL(sql, False)
        except mysql.connector.IntegrityError:
            return False
        return True

    def setBirthday(self, DiscordID, birthday):
        sql = "UPDATE `master` SET `Birthday` = '{0}' WHERE DISCORDID = '{1}'".format(birthday, DiscordID)
        self.executeSQL(sql, False)
