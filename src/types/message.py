from __future__ import annotations
import re
import functools
from typing import Any
from src.types.packet import Packet

__all__ = (
    'Message'
)


def _load_styles():
    data = {
        "0": "black",
        "1": "dark_blue",
        "2": "dark_green",
        "3": "dark_aqua",
        "4": "dark_red",
        "5": "dark_purple",
        "6": "gold",
        "7": "gray",
        "8": "dark_gray",
        "9": "blue",
        "a": "green",
        "b": "aqua",
        "c": "red",
        "d": "light_purple",
        "e": "yellow",
        "f": "white",
        "k": "obfuscated",
        "l": "bold",
        "m": "strikethrough",
        "n": "underline",
        "o": "italic",
        "r": "reset",
    }

    _code_by_name = {}
    _code_by_prop = {}
    for code, name in data.items():
        _code_by_name[name] = code
        if code in "klmnor":
            if name == "underline":
                prop = "underlined"
            else:
                prop = name
            _code_by_prop[prop] = code

    return _code_by_name, _code_by_prop


code_by_name, code_by_prop = _load_styles()


@functools.total_ordering
class Message:
    """
    A Minecraft chat message
    """

    def __init__(self, message):
        self.message = message

    @classmethod
    def from_packet(cls, packet: Packet) -> object:
        return cls(packet.unpack_json())

    @classmethod
    def from_string(cls, text) -> Message:
        """Initialize a :class:`Message` from a string"""

        return cls({'text': text})

    @classmethod
    def strip_styles(cls, text: str) -> str:
        """Remove color styles from the given text"""

        return re.sub(u'\u00A7.', '', text)

    def to_bytes(self):
        return Packet.pack_json(self.message)

    def to_string(self, strip_styles=True) -> str:
        """
        Return the actual content of the message, optionally keep the styles.
        """

        def parse(obj: Any):
            if isinstance(obj, str):
                return obj
            if isinstance(obj, list):
                return "".join((parse(e) for e in obj))
            if isinstance(obj, dict):
                text = ""
                for prop, code in code_by_prop.items():
                    if obj.get(prop):
                        text += u"\u00a7" + code
                if "color" in obj:
                    text += u"\u00a7" + code_by_name[obj["color"]]
                if "translate" in obj:
                    text += obj["translate"]
                    if "with" in obj:
                        args = u", ".join((parse(e) for e in obj["with"]))
                        text += u"{0}".format(args)
                if "text" in obj:
                    text += obj["text"]
                if "extra" in obj:
                    text += parse(obj["extra"])
                return text

        text = parse(self.message)
        if strip_styles:
            text = self.strip_styles(text)
        return text

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Message) and self.message == other.message

    def __lt__(self, other: Any) -> bool:
        return isinstance(other, Message) and self.message < other.message

    def __str__(self):
        self.to_string()

    def __repr__(self) -> str:
        return f"<Message {str(self)}>"
