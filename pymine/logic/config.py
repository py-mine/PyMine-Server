from immutables import Map
import base64
import yaml

from pymine.util.misc import java_string_hash, gen_seed

DEFAULT_CONFIG = {
    "comp_thresh": 256,
    "debug": True,
    "difficulty": "easy",
    "enable_query": True,
    "gamemode": "survival",
    "generate_structures": True,
    "generator": "default",
    "hardcore": False,
    "level_name": "world",
    "max_players": 20,
    "motd": "A Minecraft Server",
    "online_mode": True,
    "prompt": "> ",
    "pvp": True,
    "query_port": None,
    "seed": gen_seed(),
    "server_ip": None,
    "server_port": 25565,
    "spawn_animals": True,
    "spawn_monsters": True,
    "spawn_npcs": True,
    "spawn_protection": 16,
    "view_distance": 10,
    "white_list": True,
}


def load_config():  # FIXME Write directly to file with yaml lib instead of like this(can wait until we switch to new lib)
    conf = DEFAULT_CONFIG

    try:
        with open("server.yml", "r", encoding="utf8") as f:
            conf = yaml.safe_load(f.read())
    except FileNotFoundError:
        with open("server.yml", "w+") as f:
            f.write(yaml.dump(DEFAULT_CONFIG, default_style='"'))

    # Check for missing
    if any([(key not in conf) for key in DEFAULT_CONFIG.keys()]):
        conf = {**DEFAULT_CONFIG, **conf}

        with open("server.yml", "w") as f:
            f.write(yaml.dump(conf))

    if isinstance(conf["seed"], str):  # seed is str, we need int
        conf["seed"] = java_string_hash(conf["seed"][:20])

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
