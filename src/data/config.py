from immutables import Map

__all__ = ('SERVER_PROPERTIES', 'SERVER_PROPERTIES_BLANK', 'parse_properties',)

SERVER_PROPERTIES = Map({
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
