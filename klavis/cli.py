"""
Klavis CLI runner

Starts the KlavisServer with the available MIDI input (real or mock).

Usage:
    klavis-run [--mock] [--port "name"] [--quiet]
"""

import argparse
from klavis import KlavisServer, MockMidiInput, MidiEvent

def main():
    parser = argparse.ArgumentParser(
        description="Klavis MIDI event server"
    )

    parser.add_argument(
        "--mock", action="store_true",
        help="Force use of mock MIDI input"
    )

    parser.add_argument(
        "--port", type=str, default=None,
        help="Name of the MIDI port to use (partial match)"
    )

    parser.add_argument(
        "--quiet", action="store_true",
        help="Suppress event printout"
    )

    args = parser.parse_args()

    if args.mock:
        input_source = MockMidiInput()
        print("[Klavis] Using mock MIDI input.")
    else:
        try:
            from klavis import RealMidiInput
            input_source = RealMidiInput(port_name=args.port)
            print("[Klavis] Using real MIDI input.")
        except ImportError:
            print("[Klavis] RealMidiInput not available, using mock input.")
            input_source = MockMidiInput()

    def handle_event(event: MidiEvent):
        if not args.quiet:
            print("[MIDI]", event)

    server = KlavisServer(input_source)
    server.register_callback(handle_event)

    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


if __name__ == "__main__":
    main()

