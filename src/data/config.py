from immutables import Map
import base64
import yaml

__all__ = ('SERVER_PROPERTIES_DEFAULT', 'SERVER_PROPERTIES', 'FAVICON',)

SERVER_PROPERTIES_DEFAULT = Map({
    'debug': True,
    'server_ip': '0.0.0.0',
    'server_port': 25565,
    'level_name': 'world',
    'gamemode': 'survival',
    'difficulty': 'easy',
    'max_players': 20,
    'online_mode': True,
    'white_list': True,
    'motd': 'A Minecraft Server',
    'view_distance': 10,
    'spawn_protection': 16,
    'pvp': True,
    'comp_thresh': 256,
    'spawn_npcs': True,
    'spawn_animals': True,
    'spawn_monsters': True,
    'generate_structures': True,
    'support_lan': False
})


def load_properties():
    properties = SERVER_PROPERTIES_DEFAULT

    try:
        with open('server.yml', 'r') as f:
            properties = yaml.safe_load(f.read())
    except FileNotFoundError:
        with open('server.yml', 'w+') as f:
            f.write(yaml.dump(dict(SERVER_PROPERTIES_DEFAULT)))

    # Check for missing
    if any([(key not in properties) for key in SERVER_PROPERTIES_DEFAULT.keys()]):
        p_temp = properties
        properties = dict(SERVER_PROPERTIES_DEFAULT)
        properties.update(p_temp)

        with open('server.yml', 'w') as f:
            f.write(yaml.dump(properties))

    return Map(properties)


def load_favicon():
    try:
        with open('server-icon.png', 'rb') as favicon:
            return 'data:image/png;base64,' + base64.b64encode(favicon.read()).decode('utf-8')
    except FileNotFoundError:
        return None


SERVER_PROPERTIES = load_properties()
FAVICON = load_favicon()
