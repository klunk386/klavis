# Klavis

**Klavis** is a modular, Python-based MIDI event server framework.

It provides a clean architecture for receiving, processing, and routing
MIDI messages from real or simulated devices.

---

## Installation (development)

To install the package in editable mode:

```bash
pip install -e .
```

To enable real-time MIDI input with `python-rtmidi`:

```bash
pip install -e .[realtime]
```

---

## Basic Example

```python
from klavis import KlavisServer, MockMidiInput

def handle_event(event):
    print("[MIDI]", event)

server = KlavisServer(MockMidiInput())
server.register_callback(handle_event)
server.start()
```

To use a real MIDI device:

```python
from klavis import RealMidiInput

server = KlavisServer(RealMidiInput())
```

---

## Features

- Abstract input interface (`MidiInput`)
- Mock + real input sources
- Callback system for routing events
- Cross-platform support via `python-rtmidi`

---

## License

Klavis is licensed under the **GNU AGPLv3**.


