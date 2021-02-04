"""Contains packets related to teams."""

from __future__ import annotations

from pymine.types.packet import Packet
from pymine.types.buffer import Buffer
from pymine.types.chat import Chat

__all__ = ("PlayTeams",)


class PlayTeams(Packet):
    """Used to create, update, and remove teams. (Server -> Client)

    :param str team_name: The name of the team.
    :param int mode: The mode, either create team (0), remove team (1), update info (2), add entities (3), or remove entities (4)
    :param dict data: Depends on the mode, see here: https://wiki.vg/Protocol#Teams
    :ivar int id: Unique packet ID.
    :ivar int to: Packet direction.
    :ivar team_name:
    :ivar mode:
    :ivar data:
    """

    id = 0x4C
    to = 1

    def __init__(self, team_name: str, mode: int, data: dict = None) -> None:
        super().__init__()

        self.team_name = team_name
        self.mode = mode
        self.data = data

    def encode(self) -> bytes:
        out = Buffer.pack_string(self.team_name) + Buffer.pack("b", self.mode)

        if self.mode == 0:  # create team
            out += (
                Buffer.pack_chat(Chat(self.data["team_display_name"]))
                + Buffer.pack("b", self.data["friendly_flags"])
                + Buffer.pack_string(self.data["name_tag_visibility"])
                + Buffer.pack_string(self.data["collision_rule"])
                + Buffer.pack_varint(self.data["team_color"])
                + Buffer.pack_chat(Chat(self.data["team_prefix"]))
                + Buffer.pack_chat(Chat(self.data["team_suffix"]))
                + Buffer.pack_varint(len(self.data["entities"]))
                + b"".join([Buffer.pack_string(e) for e in self.data["entities"]])
            )
        elif self.mode == 2:  # update team info
            out += (
                Buffer.pack_chat(Chat(self.data["team_display_name"]))
                + Buffer.pack("b", self.data["friendly_flags"])
                + Buffer.pack_string(self.data["name_tag_visibility"])
                + Buffer.pack_string(self.data["collision_rule"])
                + Buffer.pack_varint(self.data["team_color"])
                + Buffer.pack_chat(Chat(self.data["team_prefix"]))
                + Buffer.pack_chat(Chat(self.data["team_suffix"]))
            )
        elif self.mode == 3:  # add entities to team
            out += Buffer.pack_varint(len(self.data["entities"])) + b"".join(
                [Buffer.pack_string(e) for e in self.data["entities"]]
            )
        elif self.mode == 4:  # remove entities from team
            out += Buffer.pack_varint(len(self.data["entities"])) + b"".join(
                [Buffer.pack_string(e) for e in self.data["entities"]]
            )

        return out
