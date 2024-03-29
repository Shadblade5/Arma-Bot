import json
import os

DEBUG_LOAD_CONFIG_PATH = 'C:\\Users\\Shadblade5\\github\\Arma-Bot\\config.json'


class ConfigContext():
    """A class to represent global configurations for the bot
    """

    def __init__(self, **kwargs):
        """Constructs the context

        Args:
            **TOKEN (str): Discord API Token
            **PREFIX (str): Prefix to use for commands
            **DBHOST (str): Hostname for MySQL DB
            **DBUSERNAME (str): Username for MySQL DB
            **DBPASS (str): Password for MySQL DB
        """
        self.token = kwargs['TOKEN']
        self.prefix = kwargs['PREFIX']
        self.db_host = kwargs['DBHOST']
        self.db_username = kwargs['DBUSERNAME']
        self.db_password = kwargs['DBPASS']

    def __dict__(self):
        """Returns the class in a dictionary representation

        Returns:
            Dict: Dictionary description of class
        """
        return {
            'token': self.token,
            'prefix': self.prefix,
            'db_host': self.db_host,
            'db_username': self.db_username,
            'db_password': self.db_password
        }


def load_config(filepath: str):
    cfg = None
    try:
        f = open(filepath, mode='r')
        data = json.load(f)
        cfg = ConfigContext(
            TOKEN=data['TOKEN'],
            PREFIX=data['PREFIX'],
            DBHOST=data['DBHOST'],
            DBUSERNAME=data['DBUSERNAME'],
            DBPASS=data['DBPASS']
        )
    except json.JSONDecodeError:
        print('Failed to parse JSON Configuration!\n')
    except IOError:
        print('Failed to read config file!\n')
    except LookupError:
        print('Configuration key not found!\n')
    return cfg


def create_config_from_environment():
    return ConfigContext(
        TOKEN=os.environ.get('BOT_TOKEN', ''),
        PREFIX=os.environ.get('BOT_COMMAND_PREFIX', ''),
        DBHOST=os.environ.get('BOT_DB_HOST', ''),
        DBUSERNAME=os.environ.get('BOT_DB_USERNAME', ''),
        DBPASS=os.environ.get('BOT_DB_PASSWORD', '')
    )
