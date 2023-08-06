# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

import unittest
from ..core import comPortController


class TestComPort(unittest.TestCase):
    def test_scanner(self):
        """check if a supported comport device is connected"""
        ports = comPortController.search_comports()
        self.assertTrue(type(ports) == list)
