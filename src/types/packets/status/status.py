from __future__ import annotations

from src.types.buffer import Buffer
from src.types.packet import Packet

__all__ = ('StatusStatusRequest', 'StatusStatusResponse', 'StatusStatusPingPong',)


class StatusStatusRequest(Packet):
    """Request from the client to get information on the server. (Client -> Server)

    :attr type id_: Unique packet ID.
    """

    id_ = 0x00

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def decode(cls, buf: Buffer) -> StatusStatusRequest:
        return cls()


class StatusStatusResponse(Packet):
    """Returns server status data back to the requesting client. (Server -> Client)

    :param dict response_data: JSON response data sent back to the client.
    :attr type id_: Unique packet ID.
    :attr response_data:
    """

    id_ = 0x00

    def __init__(self, response_data: dict) -> None:
        # What response_data should be like
        # {
        #     "version": {
        #         "name": "1.8.7",
        #         "protocol": 47
        #     },
        #     "players": {
        #         "max": 100,
        #         "online": 5,
        #         "sample": [
        #             {
        #                 "name": "thinkofdeath",
        #                 "id": "4566e69f-c907-48ee-8d71-d7ba5aa00d20"
        #             }
        #         ]
        #     },
        #     "description": {
        #         "text": "Hello world"
        #     },
        #     "favicon": "data:image/png;base64,<data>"
        # }

        super().__init__()

        self.response_data = response_data

    def encode(self) -> bytes:
        return Buffer.pack_json(self.response_data)


class StatusStatusPingPong(Packet):  # Client -> Server AND Server -> Client
    id_ = 0x01

    def __init__(self, payload: int) -> None:
        super().__init__()

    @classmethod
    def decode(cls, buf: Buffer) -> StatusStatusPingPong:
        return cls(buf.unpack('l'))

    def encode(self) -> bytes:
        return Buffer.pack('l', self.payload)
