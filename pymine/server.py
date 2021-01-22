import asyncio
import aiohttp
import random
import socket
import struct

from pymine.types.buffer import Buffer
from pymine.types.stream import Stream
from pymine.types.packet import Packet

from pymine.data.packet_map import PACKET_MAP
from pymine.data.states import STATES

from pymine.util.logging import task_exception_handler, Logger
from pymine.util.config import load_config, load_favicon
from pymine.util.encryption import gen_rsa_keys

from pymine.api import PyMineAPI

# Used for parts of PyMine that utilize the server instance without being a plugin themselves
server = None


class Server:
    class Meta:
        def __init__(self):
            self.server = 1
            self.version = "1.16.5"
            self.protocol = 754

    class Secrets:
        def __init__(self, rsa_private, rsa_public):
            self.rsa_private = rsa_private
            self.rsa_public = rsa_public

    class Cache:
        def __init__(self):
            self.states = {}  # {remote: state}
            self.login = {}  # {remote: {username: username, verify: verify token}}
            self.entity_id = {}  # {remote: entity_id}
            self.user_cache = {}  # {entity_id: {remote: tuple, uuid: str}}

    def __init__(self, logger):
        self.logger = logger

        self.meta = self.Meta()
        self.cache = self.Cache()
        self.secrets = self.Secrets(*gen_rsa_keys())

        self.conf = load_config()
        self.favicon = load_favicon()
        self.comp_thresh = self.conf["comp_thresh"]

        self.logger.debug_ = self.conf["debug"]

        self.aiohttp_ses = None
        self.server = None
        self.api = None

    async def start(self):
        addr = self.conf["server_ip"]
        port = self.conf["server_port"]

        if not addr:
            addr = socket.gethostbyname(socket.gethostname())

        self.aiohttp_ses = aiohttp.ClientSession()
        self.server = await asyncio.start_server(self.handle_connection, host=addr, port=port)
        self.api = PyMineAPI(self)

        await self.api.init()

        async with self.server:
            self.logger.info(f"PyMine {self.meta.server:.1f} started on {addr}:{port}!")

            self.api.taskify_handlers(self.api.events._server_ready)

            await self.server.serve_forever()

    async def stop(self):
        self.logger.info("Closing server...")

        self.server.close()
        await asyncio.gather(self.server.wait_closed(), self.api.stop(), self.aiohttp_ses.close())

        self.logger.info("Server closed.")

    async def close_connection(self, stream: Stream):  # Close a connection to a client
        await stream.drain()

        stream.close()
        await stream.wait_closed()

        try:
            del self.cache.states[stream.remote]
        except BaseException:
            pass

        self.logger.debug(f"Disconnected nicely from {stream.remote[0]}:{stream.remote[1]}.")

        return False, stream

    async def send_packet(self, stream: Stream, packet: Packet):
        self.logger.debug(f"OUT: state:unknown     | id:0x{packet.id:02X} | packet:{type(packet).__name__}")

        stream.write(Buffer.pack_packet(packet))
        await stream.drain()

    async def broadcast_packet(self, packet: Packet):
        self.logger.debug(f"OUT: state:BROADCAST   | id:0x{packet.id:02X} | packet:{type(packet).__name__}")

        raise NotImplementedError

    async def handle_packet(self, stream: Stream):  # Handle / respond to packets, this is called in a loop
        packet_length = 0

        # Basically an implementation of Buffer.unpack_varint()
        # except designed to read directly from a a StreamReader
        # and also to handle legacy server list ping packets
        for i in range(5):
            try:
                read = await asyncio.wait_for(stream.read(1), 5)
            except asyncio.TimeoutError:
                self.logger.debug("Closing due to timeout on read...")
                return False, stream

            if read == b"":
                self.logger.debug("Closing due to invalid read....")
                return False, stream

            if i == 0 and read == b"\xFE":
                self.logger.warn("Legacy ping attempted, legacy ping is not supported.")
                return False, stream

            b = struct.unpack("B", read)[0]
            packet_length |= (b & 0x7F) << 7 * i

            if not b & 0x80:
                break

        if packet_length & (1 << 31):
            packet_length -= 1 << 32

        buf = Buffer(await stream.read(packet_length))

        state = STATES.encode(states.get(stream.remote, 0))
        packet = buf.unpack_packet(state, PACKET_MAP)

        self.logger.debug(f"IN : state:{state:<11} | id:0x{packet.id:02X} | packet:{type(packet).__name__}")

        if self.api.events._packet[state].get(packet.id) is None:
            self.logger.warn(f"No valid packet handler found for packet {state} 0x{packet.id:02X} {type(packet).__name__}")
            return True, stream

        do_continue = True

        for handler in self.api.events._packet[state][packet.id]:
            try:
                continue_, stream = await handler(stream, packet)
            except BaseException as e:
                self.logger.error(
                    f"Error occurred in {handler.__module__}.{handler.__qualname__}: {self.logger.f_traceback(e)}"
                )

            if not continue_:
                do_continue = False

        return do_continue, stream

    async def handle_connection(self, reader, writer):  # Handle a connection from a client
        stream = Stream(reader, writer)
        self.logger.debug(f"Connection received from {stream.remote[0]}:{stream.remote[1]}.")

        do_continue = True

        while do_continue:
            try:
                do_continue, stream = await self.handle_packet(stream)
            except BaseException as e:
                self.logger.error(self.logger.f_traceback(e))

        await self.close_connection(stream)
