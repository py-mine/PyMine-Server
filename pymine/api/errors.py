class StopHandling(BaseException):
    pass


class InvalidPacketID(BaseException):
    pass


class ServerBindingError(BaseException):
    def __init__(self, server_name: str, addr: str, port: int):
        self.msg = f"Failed to bind {server_name} to {addr}:{port}, is that address already in use?"
        super().__init__(self.msg)


class ParsingError(BaseException):
    def __init__(self, msg: str) -> None:
        self.msg = msg
        super().__init__(self.msg)
