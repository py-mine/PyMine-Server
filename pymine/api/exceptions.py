class StopHandling(BaseException):
    pass


class InvalidPacketID(BaseException):
    pass


class ServerBindingError(BaseException):
    def __init__(self, addr: str, port: int):
        super().__init__(f"Failed to bind to {addr}:{port}")

        self.addr = addr
        self.port = port
