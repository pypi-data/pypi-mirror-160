#  telectron - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
#
#  This file is part of telectron.
#
#  telectron is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  telectron is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with telectron.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from telectron.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from telectron.raw.core import TLObject
from telectron import raw
from typing import List, Union, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class SetChatAvailableReactions(TLObject):  # type: ignore
    """Telegram API method.

    Details:
        - Layer: ``138``
        - ID: ``0x14050ea6``

    Parameters:
        peer: :obj:`InputPeer <telectron.raw.base.InputPeer>`
        available_reactions: List of ``str``

    Returns:
        :obj:`Updates <telectron.raw.base.Updates>`
    """

    __slots__: List[str] = ["peer", "available_reactions"]

    ID = 0x14050ea6
    QUALNAME = "functions.messages.SetChatAvailableReactions"

    def __init__(self, *, peer: "raw.base.InputPeer", available_reactions: List[str]) -> None:
        self.peer = peer  # InputPeer
        self.available_reactions = available_reactions  # Vector<string>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SetChatAvailableReactions":
        # No flags
        
        peer = TLObject.read(b)
        
        available_reactions = TLObject.read(b, String)
        
        return SetChatAvailableReactions(peer=peer, available_reactions=available_reactions)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Vector(self.available_reactions, String))
        
        return b.getvalue()
