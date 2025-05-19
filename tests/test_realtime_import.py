"""
Test conditional import of RealMidiInput from klavis.realtime.

This test ensures that the RealMidiInput class is available if
python-rtmidi is installed, and handles absence gracefully.
"""

import unittest


class TestRealMidiInputImport(unittest.TestCase):
    def test_import_realtime_input(self):
        try:
            from klavis.realtime import RealMidiInput
        except ImportError:
            self.skipTest("python-rtmidi is not installed")
            return

        self.assertTrue(callable(RealMidiInput))

