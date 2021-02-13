from immutables import Map
import base64
import yaml

from pymine.util.misc import string_hash_code, gen_seed

DEFAULT_CONFIG = {
    "debug": True,
    "dev_mode": True,
    "server_ip": None,
    "server_port": 25565,
    "level_name": "world",
    "seed": gen_seed(),
    "gamemode": "survival",
    "difficulty": "easy",
    "hardcore": False,
    "max_players": 20,
    "online_mode": True,
    "white_list": True,
    "motd": "A Minecraft Server",
    "view_distance": 10,
    "spawn_protection": 16,
    "pvp": True,
    "comp_thresh": 256,
    "spawn_npcs": True,
    "spawn_animals": True,
    "spawn_monsters": True,
    "generate_structures": True,
}


def load_config():
    conf = DEFAULT_CONFIG

    try:
        with open("server.yml", "r") as f:
            conf = yaml.safe_load(f.read())
    except FileNotFoundError:
        with open("server.yml", "w+") as f:
            f.write(yaml.dump(DEFAULT_CONFIG))

    # Check for missing
    if any([(key not in conf) for key in DEFAULT_CONFIG.keys()]):
        conf = {**DEFAULT_CONFIG, **conf}

        with open("server.yml", "w") as f:
            f.write(yaml.dump(conf))

    if isinstance(conf["seed"], str):  # seed is str, we need int
        conf["seed"] = string_hash_code(conf["seed"][:20])

    if conf["seed"] > 2 ** 64:  # seed is too big
        conf["seed"] = gen_seed()

        with open("server.yml", "w") as f:
            f.write(yaml.dump(conf))

    return Map(conf)


def load_favicon():
    try:
        with open("server-icon.png", "rb") as favicon:
            return "data:image/png;base64," + base64.b64encode(favicon.read()).decode("utf-8")
    except FileNotFoundError:
        return None
