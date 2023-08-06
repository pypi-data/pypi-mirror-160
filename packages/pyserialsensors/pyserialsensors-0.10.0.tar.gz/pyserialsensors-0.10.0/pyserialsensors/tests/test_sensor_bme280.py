import logging
import unittest
from unittest.mock import MagicMock
from ..devices.bme280 import BME280
from ..core.i2controller import MmsI2cController
from ..core.toolbox import scan_i2c
from ..devices.FTDI import init_all
from ..core.error import Error

logging.basicConfig(level=logging.DEBUG)


class MockTestBME280(unittest.TestCase):
    sensor_type = "BME280"

    def setUp(self):
        bus = MagicMock()
        mux = MagicMock()
        mux.__str__ = "DummyMUX"
        mux.address = 0x00
        self.sensor = BME280(bus, mux, 0x01)

    def test_measurement(self):

        self.sensor.param_t1 = 28470
        self.sensor.param_t2 = 26738
        self.sensor.param_t3 = 50
        self.sensor.param_p1 = 37529
        self.sensor.param_p2 = -10507
        self.sensor.param_p3 = 3024
        self.sensor.param_p4 = 9278
        self.sensor.param_p5 = -158
        self.sensor.param_p6 = -7
        self.sensor.param_p7 = 9900
        self.sensor.param_p8 = -10230
        self.sensor.param_p9 = 4285
        self.sensor.param_h1 = 75
        self.sensor.param_h2 = 352
        self.sensor.param_h3 = 0
        self.sensor.param_h4 = 345
        self.sensor.param_h5 = 50
        self.sensor.param_h6 = 30

        T_raw = 0x00083340
        P_raw = 0x000491D0
        H_raw = 0x00007718

        raw_data = [0x49, 0x1D, 0x00, 0x83, 0x34, 0x00, 0x77, 0x18]

        T_ref = 26.104940105066635  # °C
        P_ref = 100129.97641761282  # Pa
        H_ref = 45.058116310081616  # %

        T = self.sensor.read_temperature(raw_data)
        self.assertEqual(T - T_ref, 0)

        H = self.sensor.read_humidity(raw_data)
        self.assertEqual(H - H_ref, 0)

        P = self.sensor.read_pressure(raw_data)
        self.assertEqual(P - P_ref, 0)
