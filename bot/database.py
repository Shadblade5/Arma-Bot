from mysql import connector as sql
from datetime import datetime
import pytz


DATABASE_NAME = 'arma'


class Database:
    def __init__(self, db_host, db_username, db_password, db_name):
        self.db_host = db_host
        self.db_username = db_username
        self.db_password = db_password
        self.db_name = db_name
        self.retries = 0

    async def executeSQL(self, sql_query, query=True):
        try:
            print('Connecting to MYSQL...')
            client = sql.connect(host=self.db_host,
                                 user=self.db_username,
                                 password=self.db_password,
                                 database=self.db_name)
            print('Connected.')
            mycursor = client.cursor()
            mycursor.execute(sql_query)
            if query:
                print('Fetching data')
                return mycursor.fetchall()
            else:
                print('Commiting')
                client.commit()
        except sql.InterfaceError:
            self.retries += 1
            print(f'Failed to connect,attempt #{self.retries}. Retrying...')
            if (self.retries < 60):
                return await self.executeSQL(sql_query, query)
            else:
                print('Server unresponsive.')
        except sql.IntegrityError as e:
            print(e)
            return 1
        except sql.errors as e:
            print(e)
        finally:
            print('Closing connection')
            client.close()

    async def getUsers(self):
        sql_query = 'SELECT * FROM master'
        return await self.executeSQL(sql_query)

    async def getUserInfo(self, DiscordID):
        sql_query = f'SELECT * FROM master WHERE DISCORDID = {DiscordID}'
        results = await self.executeSQL(sql=sql_query, query=True)
        return results[0]

    async def adduser(self, DiscordID, DiscordName):
        now = datetime.now()
        dt_string = now.strftime(
            '%Y-%m-%d %H:%M:%S').astimezone(pytz.timezone('US/Eastern'))
        sql_query = f"INSERT INTO `master` VALUES ('{DiscordID}','{DiscordName}','0','0','{dt_string}','NULL');"
        if await self.executeSQL(sql_query, False) == 1:
            return False
        else:
            return True

    async def getcoc(self):
        sql_query = 'SELECT * FROM coc'
        return await self.executeSQL(sql_query)

    async def setBirthday(self, DiscordID, birthday):
        sql_query = f"UPDATE `master` SET `Birthday` = '{birthday}' WHERE DISCORDID = '{DiscordID}'"
        try:
            await self.executeSQL(sql_query, False)
        except Exception:
            return False
        return True
