from socket import gethostbyname
from steam.client import SteamClient, SteamError
from steam.game_servers import a2s_info

# Create your views here.

server_ip = gethostbyname('rcog.ddns.us')
filter_text_server = f'\\appid\\107410\\gameaddr\\{server_ip}'


async def get_servers():
    statuses = []
    client = SteamClient()
    client.anonymous_login()

    try:
        game_servers = client.gameservers.get_server_list(filter_text_server)
        if game_servers != 'None':
            for server in game_servers:
                print('\n'+str(server)+'\n')
                addr, port = server['addr'].split(':')
                info = a2s_info((addr, int(port)))
                statuses.append({
                    'name': server['name'],
                    'players': server['players'],
                    'mission': info['game'],
                    'map': server['map']
                })
    except (IndexError, SteamError, KeyError):
        print('Server offline or unreachable')
    finally:
        client.logout()
    return statuses
