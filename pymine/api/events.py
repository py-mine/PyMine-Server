from pymine.api.abc import AbstractEvent, AbstractPlugin


class GenericEvent(AbstractEvent):
    """Used to create events which take no extra parameters."""

    def __init__(self, handler):
        self.handler = handler
        self.cls = handler.__self__


class PacketEvent(AbstractEvent):
    """Triggered when an oncoming packet for the specified state id and packet id is received."""

    def __init__(self, handler, state_id: int, packet_id: int):
        self.handler = handler
        self.cls = handler.__self__
        self.state_id = state_id
        self.packet_id = packet_id


class ServerStartEvent(GenericEvent):
    """Triggered when the server starts up."""

    pass


class ServerStopEvent(GenericEvent):
    """Triggered when the server shuts down, before each plugin cog is teared down."""

    pass
