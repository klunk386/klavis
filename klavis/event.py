# *****************************************************************************
# Klavis - MIDI Event Definition
# Copyright (C) 2025, Valerio Poggi
#
# This file is part of Klavis.
#
# Klavis is free software: you can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# Klavis is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# *****************************************************************************

"""
Klavis Event Module

Defines the MidiEvent class, a basic data container for MIDI event messages.

Author: Valerio Poggi
License: AGPLv3
"""

class MidiEvent:
    """
    Represents a MIDI event with basic attributes.

    Parameters
    ----------
    type : str
        Type of MIDI message (e.g., 'note_on', 'note_off').
    note : int
        MIDI note number (e.g., 60 = Middle C).
    velocity : int
        Note velocity, ranging from 0 to 127.
    channel : int
        MIDI channel number, ranging from 0 to 15.
    timestamp : float
        Timestamp of the event in seconds since the epoch.
    """

    def __init__(
        self,
        type: str,
        note: int,
        velocity: int,
        channel: int,
        timestamp: float
    ):
        self.type = type
        self.note = note
        self.velocity = velocity
        self.channel = channel
        self.timestamp = timestamp

    def __repr__(self) -> str:
        names = ['C', 'C#', 'D', 'D#', 'E', 'F',
                 'F#', 'G', 'G#', 'A', 'A#', 'B']
        note = f"{names[self.note % 12]}{(self.note // 12) - 1}"
        ch = self.channel + 1
        return (
            f"<MidiEvent {self.type} {note} vel={self.velocity} "
            f"ch={ch} @ {self.timestamp:.3f}>"
        )

