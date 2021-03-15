import asyncio
import aiohttp
import random
import socket
import struct

from prompt_toolkit.enums import EditingMode

from pymine.types.buffer import Buffer
from pymine.types.stream import Stream
from pymine.types.packet import Packet

from pymine.util.encryption import gen_rsa_keys

from pymine.logic.config import load_config, load_favicon
from pymine.logic.worldio import load_worlds, ChunkIO
from pymine.logic.playerio import PlayerDataIO
from pymine.logic.query import QueryServer

from pymine.api.errors import StopHandling, InvalidPacketID, ServerBindingError
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

    def __init__(self, console, process_executor, thread_executor):
        self.console = console  # console instance (see pymine/api/console.py)
        self.process_executor = process_executor  # the process pool executor instance
        self.thread_executor = thread_executor  # the thread pool executor instance

        self.meta = self.Meta()
        self.cache = self.Cache()
        self.secrets = self.Secrets(*gen_rsa_keys())

        self.conf = load_config()  # contents of server.yml in the root dir
        self.favicon = load_favicon()  # server-icon.png in the root dir, displayed in clients' server lists
        self.comp_thresh = self.conf["comp_thresh"]  # shortcut for compression threshold since it's used so much

        self.console.ses.vi_mode = self.conf["vi_mode"]
        self.console.set_prompt(self.conf["prompt"])
        self.console.debug_ = self.conf["debug"]
        self.console.debug("Debug mode enabled.")

        self.port = self.conf["server_port"]
        self.addr = self.conf["server_ip"]

        if self.addr is None:  # find local addr if none was supplied
            self.addr = socket.gethostbyname(socket.gethostname())

        if self.conf["vi_mode"] == True:
            self.console.ses.editing_mode = EditingMode.VI

        self.playerio = None  # used to fetch/dump players
        self.chunkio = ChunkIO  # used to fetch chunks from the disk
        self.worlds = None  # world dictionary
        self.generator = None  # the world generator

        self.query_server = None  # the QueryServer instance
        self.api = None  # the api instance
        self.aiohttp = None  # the aiohttp session
        self.server = None  # the actual underlying asyncio server

    async def start(self):
        self.console.out.set_title(self.meta.pymine)

        try:
            self.server = await asyncio.start_server(self.handle_connection, host=self.addr, port=self.port)
        except OSError as e:
            if e.errno == 98:
                raise ServerBindingError("PyMine", self.addr, self.port)

            raise

        if self.conf["enable_query"]:
            self.query_server = QueryServer(self)
            await self.query_server.start()

        self.aiohttp = aiohttp.ClientSession()

        self.api = PyMineAPI(self)
        await self.api.init()

        # 24 / the second arg (the max chunk cache size per world instance), should be dynamically changed based on the
        # amount of players online on each world, probably something like (len(players)*24)
        self.worlds = await load_worlds(self, self.conf["level_name"], 1000)
        self.playerio = PlayerDataIO(self, self.conf["level_name"])  # Player data IO, used to load/dump player info

        try:
            self.generator = self.api.register._generators[self.conf["generator"]]
            self.console.debug(f"World generator: {self.generator.__name__}")
        except KeyError:
            self.console.error("Invalid world generator chosen in server.yml.")
            return

        self.console.info(f"PyMine {self.meta.server:.1f} started on {self.addr}:{self.port}!")

        self.api.trigger_handlers(self.api.register._on_server_start)

        try:
            await self.server.serve_forever()
        except asyncio.CancelledError:
            pass

    async def stop(self):
        self.console.info("Closing server...")

        self.api.trigger_handlers(self.api.register._on_server_stop)

        if self.server is not None:
            self.server.close()
            await self.server.wait_closed()

        if self.query_server is not None:
            self.query_server.stop()

        if self.api is not None:
            await self.api.stop()

        if self.aiohttp is not None:
            await self.aiohttp.close()

        self.console.info("Server closed.")

    async def close_connection(self, stream: Stream):  # Close a connection to a client
        try:
            await stream.drain()
        except (ConnectionResetError, BrokenPipeError):
            pass

        try:
            stream.close()
            await stream.wait_closed()
        except (ConnectionResetError, BrokenPipeError):
            pass

        try:
            del self.cache.states[stream.remote]
        except KeyError:
            pass

        try:
            del self.cache.login[stream.remote]
        except KeyError:
            pass

        try:
            del self.playerio.cache[self.cache.uuid[stream.remote]]
        except KeyError:
            pass

        try:
            del self.cache.uuid[stream.remote]
        except KeyError:
            pass

        self.console.debug(f"Disconnected nicely from {stream.remote[0]}:{stream.remote[1]}.")

        return False, stream

    async def send_packet(self, stream: Stream, packet: Packet, comp_thresh=None):
        self.console.debug(f"OUT: state:-1 | id:0x{packet.id:02X} | packet:{type(packet).__name__}")

        if comp_thresh is None:
            comp_thresh = self.comp_thresh

        stream.write(Buffer.pack_packet(packet, comp_thresh))
        await stream.drain()

    async def broadcast_packet(self, packet: Packet):  # should broadcast a packet to all connected clients in the play state
        self.console.debug(f"BROADCAST:      id:0x{packet.id:02X} | packet:{type(packet).__name__}")

        senders = []

        for p in self.playerio.cache.values():
            if p.stream is not None:
                senders.append(self.send_packet(p.stream, packet))

        await asyncio.gather(*senders)

    async def handle_packet(self, stream: Stream):  # Handle / respond to packets, this is called in a loop
        packet_length = 0

        # Basically an implementation of Buffer.unpack_varint()
        # except designed to read directly from a a StreamReader
        # and also to handle legacy server list ping packets
        for i in range(3):
            try:
                read = await asyncio.wait_for(stream.read(1), 30)
            except asyncio.TimeoutError:
                self.console.debug("Closing due to timeout on read...")
                raise StopHandling

            if read == b"":
                self.console.debug("Closing due to invalid read....")
                raise StopHandling

            if i == 0 and read == b"\xFE":
                self.console.warn("Legacy ping attempted, legacy ping is not supported.")
                raise StopHandling

            b = struct.unpack(">B", read)[0]
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
            self.console.warn("Invalid packet ID received.")
            return stream

        self.console.debug(f"IN : state: {state} | id:0x{packet.id:02X} | packet:{type(packet).__name__}")

        if self.api.register._on_packet[state].get(packet.id) is None:
            self.console.warn(f"No packet handler found for packet: 0x{packet.id:02X} {type(packet).__name__}")
            return stream

        for handler in self.api.register._on_packet[state][packet.id].values():
            try:
                res = await handler(stream, packet)

                if isinstance(res, Stream):
                    stream = res
            except StopHandling:
                raise
            except BaseException as e:
                self.console.error(
                    f"Error occurred in {handler.__module__}.{handler.__qualname__}: {self.console.f_traceback(e)}"
                )

        return stream

    async def handle_connection(self, reader, writer):  # Handle a connection from a client
        stream = Stream(reader, writer)
        self.console.debug(f"Connection received from {stream.remote[0]}:{stream.remote[1]}.")

        error_count = 0

        while True:
            try:
                stream = await self.handle_packet(stream)
            except StopHandling:
                break
            except (ConnectionResetError, BrokenPipeError):
                break
            except BaseException as e:
                error_count += 1

                self.console.error(self.console.f_traceback(e))

                if error_count > 1:
                    break

            if error_count > 0:
                error_count -= 0.5

        await self.close_connection(stream)
