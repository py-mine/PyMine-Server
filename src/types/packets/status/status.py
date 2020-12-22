from __future__ import annotations

from src.types.buffer import Buffer
from src.types.packet import Packet

__all__ = ('StatusStatus_1', 'StatusStatus_2', 'StatusStatusPingPong')

# This is just an empty packet


class StatusStatus_1(Packet):  # Client -> Server
    def __init__(self) -> None:
        super().__init__(0x00)

    @classmethod
    def decode(cls, buf: Buffer) -> StatusStatus_1:
        return cls()


class StatusStatus_2(Packet):  # Server -> Client
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

        self.response_data = response_data

    def encode(self) -> bytes:
        return Buffer.pack_json(self.response_data)


class StatusStatusPingPong(Packet):  # Client -> Server AND Server -> Client
    def __init__(self, payload: int) -> None:
        super().__init__(0x01)

    @classmethod
    def decode(cls, buf: Buffer) -> StatusStatusPingPong:
        return cls(buf.unpack('l'))

    def encode(self) -> bytes:
        return Buffer.pack('l', self.payload)
