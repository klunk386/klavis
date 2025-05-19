"""
Klavis - A modular MIDI event server and interface framework.

Provides a consistent interface for MIDI input sources, real or simulated,
and a server to dispatch events to user-defined callbacks.

Author: Valerio Poggi
License: AGPLv3
"""

from klavis.event import MidiEvent
from klavis.input import MidiInput, MockMidiInput
from klavis.server import KlavisServer

__all__ = [
    "MidiEvent",
    "MidiInput",
    "MockMidiInput",
    "KlavisServer"
]

# Try to load RealMidiInput if rtmidi is available
try:
    from klavis.realtime import RealMidiInput
    __all__.append("RealMidiInput")
except Exception as e:
    import warnings
    warnings.warn(
        f"[Klavis] RealMidiInput not available: {e}"
    )

