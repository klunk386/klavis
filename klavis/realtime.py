# *****************************************************************************
# Klavis - Real-Time MIDI Input via python-rtmidi
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
Klavis Realtime Input Module

Provides RealMidiInput for reading events from hardware devices using
python-rtmidi.

Author: Valerio Poggi
License: AGPLv3
"""

import time

from klavis.event import MidiEvent
from klavis.input import MidiInput

try:
    import rtmidi
except ImportError as e:
    raise ImportError(
        "python-rtmidi is required for RealMidiInput. "
        "Install it with: pip install python-rtmidi"
    ) from e


class RealMidiInput(MidiInput):
    """
    Real-time MIDI input using the python-rtmidi backend.

    Parameters
    ----------
    port_name : str, optional
        A string to match against the available port names. If None,
        the first available port is used.
    """

    def __init__(self, port_name: str = None):
        self.midiin = rtmidi.MidiIn()
        self.port_index = self._choose_port(port_name)
        self._safe_ignore_types(sysex=False, timing=False, sensing=False)

    def _choose_port(self, port_name: str) -> int:
        ports = self.midiin.get_ports()

        if not ports:
            raise RuntimeError("No MIDI input ports found.")

        if port_name is None:
            self._print_port_list(ports)
            print("[Klavis] No port name specified.")
            print("[Klavis] Using default port:", ports[0])
            self.midiin.open_port(0)
            return 0

        matches = [
            (i, name) for i, name in enumerate(ports)
            if port_name.lower() in name.lower()
        ]

        if not matches:
            self._print_port_list(ports)
            raise ValueError(
                f"No MIDI port matching '{port_name}' found."
            )

        if len(matches) > 1:
            print("[Klavis] Multiple ports match your input:")
            for i, name in matches:
                print(f"  [{i}] {name}")
            raise ValueError(
                f"Ambiguous port name '{port_name}'. Be more specific."
            )

        index, name = matches[0]
        self.midiin.open_port(index)
        print(f"[Klavis] Using MIDI port: {name}")
        return index

    def _print_port_list(self, ports):
        print("[Klavis] Available MIDI input ports:")
        for i, name in enumerate(ports):
            print(f"  [{i}] {name}")

    def _safe_ignore_types(self, sysex=True, timing=True, sensing=True):
        try:
            self.midiin.ignore_types(
                sysex=sysex, timing=timing, sensing=sensing)
        except TypeError:
            # Older versions of python-rtmidi do not support 'sensing'
            self.midiin.ignore_types(sysex=sysex, timing=timing)

    def read(self) -> MidiEvent:
        while True:
            result = self.midiin.get_message()
            if result is not None:
                msg, timestamp = result
                return self._parse_message(msg, timestamp)
            time.sleep(0.01)

    def _parse_message(self, msg: list, timestamp: float) -> MidiEvent:
        if not msg:
            return None

        status = msg[0] & 0xF0
        channel = msg[0] & 0x0F

        if status == 0x90 and len(msg) >= 3 and msg[2] > 0:
            return MidiEvent("note_on", msg[1], msg[2], channel, time.time())
        elif status == 0x80 and len(msg) >= 3:
            return MidiEvent("note_off", msg[1], msg[2], channel, time.time())
        elif status == 0x90 and len(msg) >= 3 and msg[2] == 0:
            return MidiEvent("note_off", msg[1], msg[2], channel, time.time())

        # Fallback for unknown/short messages
        note = msg[1] if len(msg) > 1 else 0
        velocity = msg[2] if len(msg) > 2 else 0

        return MidiEvent("unknown", note, velocity, channel, time.time())


