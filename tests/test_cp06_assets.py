from __future__ import annotations

import unittest

from scripts.cp06.check_blender_transport import parse_port


class Cp06TransportTests(unittest.TestCase):
    def test_default_port(self) -> None:
        self.assertEqual(parse_port(None), 9876)

    def test_explicit_port(self) -> None:
        self.assertEqual(parse_port("9877"), 9877)

    def test_rejects_invalid_port(self) -> None:
        with self.assertRaises(ValueError):
            parse_port("70000")


if __name__ == "__main__":
    unittest.main()
