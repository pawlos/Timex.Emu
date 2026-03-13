import tests_suite

import unittest
from ioports import IOPorts


class tests_ioports(unittest.TestCase):

    def test_port_0xff_accessible(self):
        ports = IOPorts()
        # Port 0xFF should be accessible without IndexError
        ports[0xFF] = 0x42
        self.assertEqual(0x42, ports[0xFF])

    def test_all_256_ports_exist(self):
        ports = IOPorts()
        self.assertEqual(256, len(ports.ports))
