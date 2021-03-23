# A flexible and fast Minecraft server software written completely in Python.
# Copyright (C) 2021 PyMine

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from immutables import Map
import base64
import yaml

from pymine.util.misc import java_string_hash, gen_seed

DEFAULT_CONFIG = {
    "comp_thresh": 256,
    "debug": True,
    "difficulty": "easy",
    "enable_query": True,
    "enable_rcon": True,
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
    "rcon_broadcast_to_ops": False,
    "rcon_password": "hunter2",  # Your pass here.
    "rcon_port": 15575,  # 1-6553
    "seed": gen_seed(),
    "server_ip": None,
    "server_port": 25565,
    "spawn_animals": True,
    "spawn_monsters": True,
    "spawn_npcs": True,
    "spawn_protection": 16,
    "vi_mode": False,
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
