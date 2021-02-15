import asyncio_dgram
import asyncio
import struct

from pymine.api.errors import ServerBindingError


class QueryBuffer:
    """Buffer for the query protocol, contains method for dealing with query protocol types.

    :param bytes buf:  Internal bytes object, used to store the data in the QueryBuffer.
    :ivar type pos: The position in the internal bytes/buffer object.
    :ivar buf:
    """

    def __init__(self, buf: bytes = None) -> None:
        self.buf = b"" if buf is None else buf
        self.pos = 0

    def write(self, data: bytes) -> None:
        """Writes data to the buffer.
        :param data: Data to be written to the buffer.
        :type data: bytes
        :return: None
        """

        self.buf += data

    def read(self, length: int = None) -> bytes:
        """
        Reads n bytes from the buffer, if the length is None
        then all remaining data from the buffer is sent.
        :param length: Length in bytes to be read from the buffer.
        :type length: int
        :return: bytes
        """

        try:
            if length is None:
                length = len(self.buf)
                return self.buf[self.pos :]

            return self.buf[self.pos : self.pos + length]
        finally:
            self.pos += length

    def reset(self) -> None:
        """Resets the position in the buffer."""

        self.pos = 0

    @staticmethod
    # Why is short the only little-endian one? Nobody knows.
    def pack_short(short: int) -> bytes:
        return struct.pack("<h", short)

    def unpack_short(self) -> int:
        return struct.unpack("<h", self.read(2))[0]

    @staticmethod
    def pack_magic() -> bytes:
        return b"\xFE\xFD"  # I blame minecraft not me
        # More straightforward, but slower:
        # struct.pack('>H', 65527)

    def unpack_magic(self) -> int:
        magic = struct.unpack(">H", self.read(2))[0]

        if magic != 65277:
            raise ValueError(f"{magic} is not 65277")

        return magic

    @staticmethod
    def pack_string(string: str) -> bytes:
        return bytes(str(string), "latin-1") + b"\x00"

    def unpack_string(self) -> str:
        out = b""

        while True:
            b = self.read(1)
            if b == b"\x00":  # null byte, end of string
                break
            out += b

        return out.decode("latin-1")

    @staticmethod
    def pack_int32(num: int) -> bytes:
        return struct.pack(">i", num)

    def unpack_int32(self) -> int:
        return struct.unpack(">i", self.read(4))[0]

    @staticmethod
    def pack_byte(byte: int) -> bytes:
        return struct.pack(">b", byte)

    def unpack_byte(self) -> int:
        return struct.unpack(">b", self.read(1))[0]


class QueryServer:
    """A query server that supports the Minecraft query protocol.

    :param object server: The PyMine server instance.
    :attr object conf: The contents of server.yml (The server configuration).
    :attr object logger: The instance of the logger.
    :attr server:
    """

    def __init__(self, server):
        self.server = server  # The PyMine server instance
        self.logger = server.logger  # Logger() instance created by Server.

        self.addr = server.addr
        self.port = server.conf.get("query_port")

        if self.port is None:
            self.port = server.port

        self._server = None  # the result of asyncio_dgram.bind(...) (a stream)
        self.server_task = None  # the task that handles packets

        self.challenge_cache = {}  # {remote_ip: challenge_token (string)}

    async def start(self):
        try:
            self._server = await asyncio_dgram.bind((self.addr, self.port))
        except OSError:
            raise ServerBindingError("query server", self.addr, self.port)

        self.logger.info(f"Query server started on {self.addr}:{self.port}.")

        self.server_task = asyncio.create_task(self.handle())

    async def handle(self):
        try:
            while True:
                data, remote = await self._server.recv()
                asyncio.create_task(self.handle_packet(remote, QueryBuffer(data)))
        except asyncio.CancelledError:
            pass
        except BaseException as e:
            self.logger.error(f"Error occurred while handling query packets: {self.logger.f_traceback(e)}")

    async def handle_packet(self, remote: tuple, buf: QueryBuffer) -> None:
        try:
            try:
                buf.unpack_magic()
            except ValueError:
                self.logger.debug("Invalid value for magic recieved, continuing like nothing happened.")
                return

            packet_type = buf.unpack_byte()  # should be 9 (handshake) or 0 (stat)
            session_id = buf.unpack_int32()

            if buf.buf[buf.pos:] == b'':
                challenge_token = 0
            else:
                challenge_token = buf.unpack_int32()

            if packet_type == 9:  # handshake
                self.challenge_cache[remote] = challenge_token

                print(buf.buf[buf.pos :])

                await self._server.send(
                    (QueryBuffer.pack_byte(9) + QueryBuffer.pack_int32(session_id) + QueryBuffer.pack_string(challenge_token)),
                    remote,
                )
            elif packet_type == 0:  # respond with a stat packet
                if self.challenge_cache.get(remote) != challenge_token:
                    self.logger.warn(f"Invalid challenge token {challenge_token} received for remote {remote}")
                    return

                if buf.buf[buf.pos:buf.pos+4] == b'\x00\x00\x00\x00':  # full stat
                    out = (
                        QueryBuffer.pack_byte(packet_type)
                        + QueryBuffer.pack_int32(session_id)
                        + b'\x73\x70\x6C\x69\x74\x6E\x75\x6D\x00\x80\x00'  # constant data / padding
                        + QueryBuffer.pack_string("hostname")
                        + QueryBuffer.pack_string(self.server.conf["motd"])
                        + QueryBuffer.pack_string("game type")
                        + QueryBuffer.pack_string("SMP")
                        + QueryBuffer.pack_string("game_id")
                        + QueryBuffer.pack_string("MINECRAFT")
                        + QueryBuffer.pack_string("version")
                        + QueryBuffer.pack_string(self.server.meta.version)
                        + QueryBuffer.pack_string("plugins")
                        + QueryBuffer.pack_string("")  # empty for now
                        + QueryBuffer.pack_string("map")
                        + QueryBuffer.pack_string(self.server.conf["level_name"])
                        + QueryBuffer.pack_string("numplayers")
                        + QueryBuffer.pack_string(len(self.server.cache.states))
                        + QueryBuffer.pack_string("maxplayers")
                        + QueryBuffer.pack_string(self.server.conf["max_players"])
                        + QueryBuffer.pack_string("hostport")
                        + QueryBuffer.pack_string(self.server.port)
                        + QueryBuffer.pack_string("hostip")
                        + QueryBuffer.pack_string(self.server.addr)
                        + b'\x00'
                        + b"\x01\x70\x6C\x61\x79\x65\x72\x5F\x00\x00"  # more constant data / padding / whatever
                        + b"Penis\x00\x00"  # should be player section, this means no players online
                    )

                    await self._server.send(out, remote)
                else:
                    print("regular shit")

                await asyncio.sleep(.5)

        except asyncio.CancelledError:
            pass
        except BaseException as e:
            self.logger.error(f"Error while handling query packet: {self.logger.f_traceback(e)}")

    def stop(self):
        self.logger.debug("Query server shutting down.")
        self.server_task.cancel()
        self.server.close()
        self.logger.debug("Query server shut down successfully.")
