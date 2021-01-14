from __future__ import annotations
import re

from pymine.types.buffer import Buffer
from pymine.data.formats import *


class Chat:
    """A Minecraft chat message.

    :param object msg: dict or list object representing chat message json data.
    :attr msg:
    """

    def __init__(self, msg: object) -> None:
        self.msg = msg

    @classmethod
    def from_buf(cls, buf: 'Buffer') -> Chat:
        """Creates a Minecraft chat message from a buffer."""

        return cls(buf.unpack_json())

    @classmethod
    def from_string(cls, text: str) -> Chat:
        """Creates a Minecraft chat message from json."""

        return cls({'text': text})

    # For mode arg
    # 'plain' = plain text, no formatting
    # 'normal' = with formatting codes
    # 'color' = formatted with ansi/terminal formatting codes
    def to_string(self, mode: str) -> str:
        """Converts a Minecraft chat message to text."""

        def parse(msg):
            if isinstance(msg, str):
                if mode == 'plain':
                    return re.sub('§.', '', msg)

                if mode == 'normal':
                    return self.msg

                if mode == 'color':
                    colored = ''

                    for i, c in enumerate(msg):
                        if c == '§':
                            colored += TERMINAL_CODES[msg[i + 1]]
                            continue

                    return colored
            elif isinstance(msg, list):
                return ''.join(parse(e) for e in msg)
            elif isinstance(msg, dict):
                text = ''

                if mode != 'plain':
                    for name, code in FORMAT_BY_NAME.items():
                        if msg.get(name):
                            text += '§' + code

                if 'text' in msg:
                    text += parse(msg['text'])

                if 'extra' in msg:
                    text += parse(msg['extra'])
            elif msg is None:
                return ''
            else:
                return str(self.msg)

        return parse(self.msg)
