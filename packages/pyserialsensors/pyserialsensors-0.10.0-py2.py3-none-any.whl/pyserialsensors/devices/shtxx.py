# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
# SPDX-License-Identifier: MIT


"""
SHT85 - Humidty and Temperature sensors
class includes the function to control the SHT85 humidity sensors via I2C
"""

from ..core.error import Error
from ..core.sensor import I2CSensor


try:
    import struct
except ImportError:
    import ustruct as struct


class SHT85(I2CSensor):
    __name__ = "SHT85"
    _SENSOR_ADDRESS = 0x44
    _i2c_freq = 1e5
    _units = {"humidity": "pct", "temperature": "C"}

    def __init__(self, *args, heater_status=False, mode="ART", **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        self.exists = self.sensor_exists()
        self.mode = mode
        self.heater_status = heater_status

    def sensor_exists(self):
        """
        test if sensor is plugged on and works proper
        :return: [BOOLEAN] True if test was successful otherwise False
        """
        sn = self.get_serial_number()
        self._logger.info("Read serial number: %s", sn)

        if isinstance(sn, int):
            return True
        else:
            self.error = Error().read(self)
            return False

    def reset(self):
        """
        Reseting the sensor

        Returns:
            bool: True for successful reset else False
        """
        try:
            self.txrx([0x30, 0xA2], readlen=0)
            return True
        except IOError:
            return False

    def heater(self):
        if self.heater_status == True:
            self.txrx([0x30, 0x6D], readlen=0)
        else:
            self.txrx([0x30, 0x66], readlen=0)
        return self.heater_status

    def get_serial_number(self):
        """
        Reads unique serial number of sensor

        Returns:
             str: serial number of the sensor
        """

        self.serial_number = None
        self.error = None
        ba = self.txrx([0x36, 0x82], readlen=6)
        if ba:
            check0 = Error.checksum(byte_values=[ba[0], ba[1]], crc_value=ba[2])
            check1 = Error.checksum(byte_values=[ba[3], ba[4]], crc_value=ba[5])
            if check0[1] and check1[1]:
                binary_str = ""
                for i in [4, 3, 1, 0]:
                    bybi = str(bin(ba[i])[2:])
                    binary_str += bybi.zfill(8)[::-1]
                self.serial_number = int(binary_str, 2)
                return self.serial_number
            else:
                self.error = Error().crc(self)
                return self.error
        else:
            self.error = Error().read(self)
            return self.error

    def prepare_measurement(self):
        """
        Initializes a continuous measurement of the mass flow

        Returns:
            bool: continuous measurement established (True = successful | False = failed)
        """

        try:
            self.heater()
            self.exists = self.sensor_exists()
            self.txrx([0x2B, 0x32], readlen=0)
            return True
        except IOError:
            return False

    def get_data(self, scale_factor: int = 175, offset: int = -45):
        """Read temperature and humidty from sensor

        Args:
            scale_factor (int): sensor specific parameter for the calculation of the volume flow
            offset (int): sensor specific parameter for the calculation of the volume flow

        Returns:
            dict: data dictionary
        """

        data = None
        max_attempts = 10
        attempts = 0
        self.data = self.default_data()

        while not data and attempts < max_attempts:
            attempts += 1
            data = self.txrx([], readlen=6)

        if data is not None and len(data) == 6:
            check0 = Error.checksum([data[0], data[1]], data[2])
            check1 = Error.checksum([data[3], data[4]], data[5])
            if check0[1] and check1[1]:
                T_raw, crc0, RH_raw, crc1 = struct.unpack(">HBHB", data)
                T = round(offset + (scale_factor * (T_raw / 65535.0)), 3)
                RH = round(100 * (RH_raw / 65523.0), 3)
                self.data["values"] = {}
                self.data["values"]["humidity"] = {
                    "value": RH,
                    "unit": self._units["humidity"],
                }
                self.data["values"]["temperature"] = {
                    "value": T,
                    "unit": self._units["temperature"],
                }
                self.data["error"] = False
                return self.data
            else:
                self.reset()
                self.prepare_measurement()
                self.error = Error().crc(self)
                return self.error

        else:
            self.error = Error().read(self)
            return self.error
