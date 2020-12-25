from immutables import Map

__all__ = ('SERVER_PROPERTIES', 'SERVER_PROPERTIES_BLANK', 'parse_properties')

def parse_properties(lines):
    properties = {}

    for line in lines:
        if not line.startswith('#'):
            split = line.split('=')

            if len(split) < 1:
                raise Exception

            prop = split[0]

            if prop == '':
                raise Exception

            value = ''.join(split[1:])

            try:  # Try to convert to int
                value = int(value)
            except Exception:
                pass

            if value == 'true':  # Convert to bool
                value = True
            elif value == 'false':
                value = False

            if value == '':  # Convert to None
                value = None

            properties[prop] = value

    return properties

SERVER_PROPERTIES_BLANK = """#Minecraft server properties
spawn-protection=16
max-tick-time=60000
query.port=25565
generator-settings=
sync-chunk-writes=true
force-gamemode=false
allow-nether=true
enforce-whitelist=false
gamemode=survival
broadcast-console-to-ops=true
enable-query=false
player-idle-timeout=0
difficulty=easy
spawn-monsters=true
broadcast-rcon-to-ops=true
op-permission-level=4
pvp=true
entity-broadcast-range-percentage=100
snooper-enabled=true
level-type=default
hardcore=false
enable-status=true
enable-command-block=false
max-players=20
network-compression-threshold=256
resource-pack-sha1=
max-world-size=29999984
function-permission-level=2
rcon.port=25575
server-port=25565
debug=false
server-ip=0.0.0.0
spawn-npcs=true
allow-flight=false
level-name=world
view-distance=10
resource-pack=
spawn-animals=true
white-list=false
rcon.password=
generate-structures=true
max-build-height=256
online-mode=true
level-seed=
use-native-transport=true
prevent-proxy-connections=false
enable-jmx-monitoring=false
enable-rcon=false
motd=A Minecraft Server"""

SERVER_PROPERTIES = Map(parse_properties(SERVER_PROPERTIES_BLANK.split('\n')))
