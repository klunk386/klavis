# *****************************************************************************
# Klavis - MIDI Input Interface
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
Klavis Input Module

Defines the abstract base class MidiInput and a mock implementation for
simulated MIDI events.

Author: Valerio Poggi
License: AGPLv3
"""

import time
import random
from klavis.event import MidiEvent


class MidiInput:
    """
    Abstract base class for MIDI input sources.

    Subclasses must implement the read() method to return a MidiEvent.
    """

    def read(self) -> MidiEvent:
        """
        Read and return a new MIDI event.

        Returns
        -------
        MidiEvent
            A new MIDI event.

        Raises
        ------
        NotImplementedError
            If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Subclasses must implement the read() method.")


class MockMidiInput(MidiInput):
    """
    Simulated MIDI input that generates random note_on events at intervals.
    """

    def read(self) -> MidiEvent:
        """
        Generate a random note_on event after a short delay.

        Returns
        -------
        MidiEvent
            A randomly generated MIDI note_on event.
        """
        time.sleep(0.5)
        return MidiEvent(
            type="note_on",
            note=random.randint(60, 72),
            velocity=random.randint(80, 127),
            channel=0,
            timestamp=time.time()
        )

