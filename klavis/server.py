# *****************************************************************************
# Klavis - MIDI Event Server
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
Klavis Server Module

This module defines the KlavisServer class, which handles MIDI event polling
from an input source and dispatches them to registered callback functions.

The server supports any input source implementing the MidiInput interface.

Author: Valerio Poggi
License: AGPLv3
"""

from typing import Callable, List
from klavis.event import MidiEvent
from klavis.input import MidiInput


class KlavisServer:
    """
    MIDI event server that polls input and dispatches events.

    Parameters
    ----------
    midi_input : MidiInput
        The input device or stream providing MIDI events.
    """

    def __init__(self, midi_input: MidiInput):
        self.midi_input = midi_input
        self.callbacks: List[Callable[[MidiEvent], None]] = []
        self.running = False

    def register_callback(self, callback: Callable[[MidiEvent], None]) -> None:
        """
        Register a callback function to receive MIDI events.

        Parameters
        ----------
        callback : Callable[[MidiEvent], None]
            A function that accepts a MidiEvent instance.
        """
        self.callbacks.append(callback)

    def start(self) -> None:
        """
        Start the event loop, polling for MIDI events and dispatching them.
        """
        self.running = True
        print("[Klavis] Event loop started.")
        try:
            while self.running:
                event = self.midi_input.read()
                if event:
                    self._log_event(event)
                    self._dispatch(event)
        except KeyboardInterrupt:
            print("\n[Klavis] Interrupted by user.")
            self.stop()

    def stop(self) -> None:
        """
        Stop the event loop.
        """
        print("[Klavis] Event loop stopped.")
        self.running = False

    def _log_event(self, event: MidiEvent) -> None:
        """
        Print the received MIDI event to the console.

        Parameters
        ----------
        event : MidiEvent
            The MIDI event to be logged.
        """
        print("[Klavis] Event:", event)

    def _dispatch(self, event: MidiEvent) -> None:
        """
        Dispatch the MIDI event to all registered callback functions.

        Parameters
        ----------
        event : MidiEvent
            The MIDI event to be sent to callbacks.
        """
        for callback in self.callbacks:
            callback(event)

