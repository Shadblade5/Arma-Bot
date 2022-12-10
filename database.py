import mysql.connector as MYSQL
import config
from datetime import datetime
import pytz

class Database:
    def __init__(self, db_host, db_username, db_password,db_name):
        self.db_host     = db_host
        self.db_username = db_username
        self.db_password = db_password
        self.db_name     = db_name
        self.retries = 0

    async def executeSQL(self, sql, query=True):
        try:
            client = MYSQL.connect(host     =self.db_host,
                                   user     =self.db_username,
                                   password =self.db_password,
                                   database =self.db_name)
            print("Connected to MYSQL")
            mycursor = client.cursor()
            mycursor.execute(sql)
            if query==True:
                print("Fetching data")
                return mycursor.fetchall()
            else:
                print("Commiting")
                client.commit()
        except MYSQL.InterfaceError as err:
            print(err)
            retries += 1
            if(retries<60):
                self.executeSQL()
        except MYSQL.IntegrityError as e:
            print(e)
            return 1
        except MYSQL.errors as e:
            print(e)
        finally:
            print("Closing connection")
            client.close()

    async def getUsers(self):
        sql = "SELECT * FROM master"
        return await self.executeSQL(sql)

    async def getUserInfo(self, DiscordID):
        sql = 'SELECT * FROM master WHERE DISCORDID = {}'.format(DiscordID)
        results = await self.executeSQL(sql=sql,query=True)
        return results[0]

    async def adduser(self, DiscordID, DiscordName):
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S").astimezone(pytz.timezone('US/Eastern'))
        sql = "INSERT INTO `master` VALUES ('{0}','{1}','0','0','{2}','NULL');".format(DiscordID,DiscordName,dt_string)
        if  await self.executeSQL(sql, False) == 1:
            return False
        else:
            return True
    async def getcoc(self):
        sql = "SELECT * FROM coc"
        return await self.executeSQL(sql)


    async def setBirthday(self, DiscordID, birthday):
        sql = "UPDATE `master` SET `Birthday` = '{0}' WHERE DISCORDID = '{1}'".format(birthday, DiscordID)
        try:
            await self.executeSQL(sql, False)
        except error:
            return False
        else:
            return True

