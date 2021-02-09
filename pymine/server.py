import asyncio
import aiohttp
import random
import socket
import struct

from pymine.types.buffer import Buffer
from pymine.types.stream import Stream
from pymine.types.packet import Packet

from pymine.util.logging import task_exception_handler, Logger
from pymine.util.encryption import gen_rsa_keys

from pymine.logic.config import load_config, load_favicon
from pymine.logic.worldio import load_worlds, ChunkIO
from pymine.logic.playerio import PlayerDataIO

from pymine.api.exceptions import StopHandling, InvalidPacketID
from pymine.net.packet_map import PACKET_MAP
from pymine.api import PyMineAPI

# Used for parts of PyMine that utilize the server instance without being a plugin themselves
server = None


class Server:
    class Meta:
        def __init__(self):
            self.server = 0.1
            self.version = "1.16.5"
            self.protocol = 754
            self.pymine = f"PyMine {self.server}"

    class Secrets:
        def __init__(self, rsa_private, rsa_public):
            self.rsa_private = rsa_private
            self.rsa_public = rsa_public

    class Cache:
        def __init__(self):
            self.states = {}  # {remote: state}
            self.login = {}  # {remote: {username: username, verify: verify token}}
            self.uuid = {}  # {remote: uuid as int}

    def __init__(self, logger, executor, uvloop):
        self.logger = logger  # logger instance
        self.executor = executor  # the process pool executor instance
        self.uvloop = uvloop  # bool whether uvloop is being used or not

        self.meta = self.Meta()
        self.cache = self.Cache()
        self.secrets = self.Secrets(*gen_rsa_keys())

        self.conf = load_config()  # contents of server.yml in the root dir
        self.favicon = load_favicon()  # server-icon.png in the root dir, displayed in clients' server lists
        self.comp_thresh = self.conf["comp_thresh"]  # shortcut for compression threshold since it's used so much

        self.logger.debug_ = self.conf["debug"]
        asyncio.get_event_loop().set_debug(self.conf["debug"])

        self.playerio = None  # used to fetch/dump players
        self.chunkio = ChunkIO  # used to fetch chunks from the disk
        self.worlds = None  # world dictionary

        self.aiohttp = None  # the aiohttp session
        self.server = None  # the actual underlying asyncio server
        self.api = None  # the api instance

    async def start(self):
        addr = self.conf["server_ip"]
        port = self.conf["server_port"]

        if not addr:  # find local ip if none was supplied
            addr = socket.gethostbyname(socket.gethostname())

        self.aiohttp = aiohttp.ClientSession()
        self.server = await asyncio.start_server(self.handle_connection, host=addr, port=port)
        self.api = PyMineAPI(self)

        await self.api.init()

        # 24 / the second arg (the max chunk cache size per world instance), should be dynamically changed based on the
        # amount of players online on each world, probably something like (len(players)*24)
        self.worlds = await load_worlds(self, self.conf["level_name"], 24)

        # Player data IO, used to load/dump player info
        self.playerio = PlayerDataIO(self, self.conf["level_name"])

        self.logger.info(f"PyMine {self.meta.server:.1f} started on {addr}:{port}!")

        self.api.taskify_handlers(self.api.events._server_ready)

        await self.server.serve_forever()

    async def stop(self):
        self.logger.info("Closing server...")

        self.server.close()
        await asyncio.gather(self.server.wait_closed(), self.api.stop(), self.aiohttp.close())

        self.logger.info("Server closed.")

    async def close_connection(self, stream: Stream):  # Close a connection to a client
        await stream.drain()

        stream.close()
        await stream.wait_closed()

        try:
            del self.cache.states[stream.remote]
        except KeyError:
            pass

        try:
            del self.cache.login[stream.remote]
        except KeyError:
            pass

        self.logger.debug(f"Disconnected nicely from {stream.remote[0]}:{stream.remote[1]}.")

        return False, stream

    async def send_packet(self, stream: Stream, packet: Packet, comp_thresh=None):
        self.logger.debug(f"OUT: state:-1 | id:0x{packet.id:02X} | packet:{type(packet).__name__}")

        if comp_thresh is None:
            comp_thresh = self.comp_thresh

        stream.write(Buffer.pack_packet(packet, comp_thresh))
        await stream.drain()

    async def broadcast_packet(self, packet: Packet):  # should broadcast a packet to all connected clients in the play state
        self.logger.debug(f"BROADCAST:      id:0x{packet.id:02X} | packet:{type(packet).__name__}")

        raise NotImplementedError

    async def handle_packet(self, stream: Stream):  # Handle / respond to packets, this is called in a loop
        packet_length = 0

        # Basically an implementation of Buffer.unpack_varint()
        # except designed to read directly from a a StreamReader
        # and also to handle legacy server list ping packets
        for i in range(3):
            try:
                read = await asyncio.wait_for(stream.read(1), 5)
            except asyncio.TimeoutError:
                self.logger.debug("Closing due to timeout on read...")
                raise StopHandling

            if read == b"":
                self.logger.debug("Closing due to invalid read....")
                raise StopHandling

            if i == 0 and read == b"\xFE":
                self.logger.warn("Legacy ping attempted, legacy ping is not supported.")
                raise StopHandling

            b = struct.unpack("B", read)[0]
            packet_length |= (b & 0x7F) << 7 * i

            if not b & 0x80:
                break

        if packet_length & (1 << 31):
            packet_length -= 1 << 32

        buf = Buffer(await stream.read(packet_length))

        state = self.cache.states.get(stream.remote, 0)

        try:
            packet = buf.unpack_packet(state, PACKET_MAP)
        except InvalidPacketID:
            self.logger.warn("Invalid packet ID received.")
            return stream

        self.logger.debug(f"IN : state: {state} | id:0x{packet.id:02X} | packet:{type(packet).__name__}")

        if self.api.events._packet[state].get(packet.id) is None:
            self.logger.warn(f"No packet handler found for packet: 0x{packet.id:02X} {type(packet).__name__}")
            return stream

        for handler in self.api.events._packet[state][packet.id]:
            try:
                res = await handler(stream, packet)

                if isinstance(res, Stream):
                    stream = res
            except StopHandling:
                raise
            except BaseException as e:
                self.logger.error(
                    f"Error occurred in {handler.__module__}.{handler.__qualname__}: {self.logger.f_traceback(e)}"
                )

        return stream

    async def handle_connection(self, reader, writer):  # Handle a connection from a client
        stream = Stream(reader, writer)
        self.logger.debug(f"Connection received from {stream.remote[0]}:{stream.remote[1]}.")

        while True:
            try:
                stream = await self.handle_packet(stream)
            except StopHandling:
                break
            except BaseException as e:
                self.logger.error(self.logger.f_traceback(e))

        await self.close_connection(stream)
