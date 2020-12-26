from immutables import Map
import yaml

__all__ = ('SERVER_PROPERTIES_DEFAULT', 'SERVER_PROPERTIES',)

SERVER_PROPERTIES_DEFAULT = Map({
    'debug': True,
    'server_ip': '0.0.0.0',
    'level_name': 'world',
    'gamemode': 'survival',
    'difficulty': 'easy',
    'max_players': 20,
    'online_mode': True,
    'white_list': True,
    'motd': 'A Minecraft Server'
    'view_distance': 10,
    'spawn_protection': 16,
    'pvp': True,
    'comp_thresh': 256,
    'spawn_npcs': True,
    'spawn_animals': True,
    'spawn_monsters': True,
    'generate_structures': True,
})


def load_properties():
    try:
        with open('server.yml', 'r') as f:
            properties = dict(SERVER_PROPERTIES_DEFAULT)
            properties.update(yaml.load(f.read()))
            return properties
    except FileNotFoundError:
        return SERVER_PROPERTIES_DEFAULT


SERVER_PROPERTIES = load_properties()
