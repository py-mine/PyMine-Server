# A flexible and fast Minecraft server software written completely in Python.
# Copyright (C) 2021 PyMine

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations
import re

from pymine.data.formats import TERMINAL_CODES, FORMAT_BY_NAME


class Chat:
    """A Minecraft chat message.

    :param object msg: dict or list or str object representing chat message json data.
    :ivar msg:
    """

    def __init__(self, msg: object) -> None:
        if isinstance(msg, str):
            self.msg = {"text": msg}
        else:
            self.msg = msg

    @classmethod
    def from_string(cls, text: str) -> Chat:
        """Creates a Minecraft chat message from json."""

        return cls({"text": text})

    # For mode arg
    # 'plain' = plain text, no formatting
    # 'normal' = with formatting codes
    # 'color' = formatted with ansi/terminal formatting codes
    def to_string(self, mode: str) -> str:
        """Converts a Minecraft chat message to text."""

        def parse(msg):
            if isinstance(msg, str):
                if mode == "plain":
                    return re.sub("§.", "", msg)

                if mode == "normal":
                    return self.msg

                if mode == "color":
                    colored = ""

                    for i, c in enumerate(msg):
                        if c == "§":
                            colored += TERMINAL_CODES[msg[i + 1]]
                            continue

                    return colored
            elif isinstance(msg, list):
                return "".join([parse(e) for e in msg])
            elif isinstance(msg, dict):
                text = ""

                if mode != "plain":
                    for name, code in FORMAT_BY_NAME.items():
                        if msg.get(name):
                            text += "§" + code

                if "text" in msg:
                    text += parse(msg["text"])

                if "extra" in msg:
                    text += parse(msg["extra"])
            elif msg is None:
                return ""
            else:
                return str(self.msg)

        return parse(self.msg)
