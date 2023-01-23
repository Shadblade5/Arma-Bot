import json


class ConfigClass:
    def __init__(self, token, prefix, db_host, db_username, db_password):
        self.token = token
        self.prefix = prefix
        self.db_host = db_host
        self.db_username = db_username
        self.db_password = db_password


with open('../../../../config.json') as f:
    data = json.load(f)
    c = ConfigClass(data["TOKEN"], data["PREFIX"], data["DBHOST"], data["DBUSERNAME"], data["DBPASS"])
