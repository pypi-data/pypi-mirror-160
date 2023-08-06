# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT


from .MUX import TCA9548 as MUX
import time
from ..core.error import Error
from ..core.sensor import I2CSensor
from typing import Union

# import logging
# logging.basicConfig(level=logging.DEBUG)

try:
    import struct
except ImportError:
    import ustruct as struct


class SFM(I2CSensor):
    __name__ = "SFM"
    _serial_mode = "I2C"
    _SENSOR_ADDRESS = 0x40
    _units = {
        "volumeflow": "slm",
    }
    _i2c_freq = 4e5
    _offset = None
    _scale = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.reset()
        self.exists = self.sensor_exists()

    def sensor_exists(self) -> bool:
        """
        Test if sensor is plugged on and works proper

        Returns:
            bbol: True if test was successful, false otherwise.
        """
        serial_number = self.get_serial_number()
        attempt = 0
        while attempt < self._max_attempts:
            if isinstance(serial_number, int) and serial_number != 0:
                self._logger.info("Serial number: %s", serial_number)
                self.prepare_measurement()
                return True
            else:
                self._logger.warning("Reading serial number failed. Resetting...")
                rst = self.reset()
                self._logger.debug("Reset status: %s", rst)
                attempt += 1
                serial_number = self.get_serial_number()

        self.error = Error().crc(self)
        return False

    def reset(self) -> bool:
        """
        Reseting the sensor

        Returns:
            bool: True for successful reset else False
        """

        try:
            self.txrx([0x20, 0x00], readlen=0)
            time.sleep(0.1)
            return True
        except IOError:
            return False

    def get_serial_number(self) -> Union[str, None]:
        """
        Reads unique serial number of sensor.

        Returns:
            str: Serial number of the sensor
        """

        serial_number = 0
        self.error = None
        data = self.txrx([0x31, 0xAE], readlen=6)
        if data is not None:
            check = [
                Error.checksum([data[0], data[1]], data[2], crc_init=0x00)[1],
                Error.checksum([data[3], data[4]], data[5], crc_init=0x00)[1],
            ]
            if False not in check:
                serial_number = data[0]
                for i in [1, 3, 4]:
                    serial_number <<= 8
                    serial_number += data[i]
                self.serial_number = serial_number
            else:
                self._logger.warning("CRC failed while serial number is read")
                self.error = Error().crc(self)
        else:
            self.error = Error().read(self)

        self._logger.debug("Got serial number: %s", serial_number)
        return serial_number

    def prepare_measurement(self) -> bool:
        """
        Initializes a continuous measurement of the mass flow.

        Returns:
            bool: Continuous measurement established (True = successful | False = failed)
        """

        self._scale = self.get_scale_factor()
        if self._scale is None:
            return self.error

        self._offset = self.get_offset()
        if self._offset is None:
            return self.error

        data = self.txrx([0x10, 0x00], readlen=3)
        attempts = 0
        while data is None:
            attempts += 1
            data = self.txrx([0x10, 0x00], readlen=3)
            self._logger.warning(
                "Failed to prepare measurement (%s/%s).", attempts, self._max_attempts
            )
            if attempts > self._max_attempts:
                self.mux.close_all_ports()
                self.error = Error().read(self)
                break

        if data is not None and 0xFF not in data[:2]:
            self._logger.info("Started measurement cycle.")
            return True
        else:
            self.mux.close_all_ports()
            self.error = Error().read(self)
            self._logger.warning("Failed to initialize measurement cycle.")

        return self.error

    def get_scale_factor(self) -> Union[int, None]:
        """
        Read conversion factor from sensor.

        Returns:
            (int, None): Scale factor or in case of an error None
        """

        data = self.txrx([0x30, 0xDE], readlen=3)
        if Error.checksum([data[0], data[1]], data[2], crc_init=0x00)[1]:
            scale_factor = self.bytes_to_u16(data[0], data[1])
            return scale_factor
        else:
            self.error = Error().crc
            return None

    def get_offset(self) -> Union[int, None]:
        """
        Read offset value from sensor.

        Returns:
            (int, None): Scale factor or in case of an error None
        """

        data = self.txrx([0x30, 0xDF], readlen=3)
        if Error.checksum([data[0], data[1]], data[2], crc_init=0x00)[1]:
            offset = self.bytes_to_u16(data[0], data[1])
            return offset
        else:
            self.error = Error().crc
            return None

    def get_data(self) -> dict:
        """
        Read data array.

        Returns:
            dict: Data dictionary
        """

        res = self.txrx([], readlen=3)
        self._logger.debug("Result bytes: %s", res)
        self.data = self.default_data()

        if res is not None:
            if Error.checksum([res[0], res[1]], res[2], crc_init=0x00)[1]:
                value, crc = struct.unpack(">HB", res)
                flow = round((value - self._offset) / self._scale, 3)
                if flow <= -218.807:
                    self.reset()
                    self.prepare_measurement()
                    self.error = Error().read(self)
                    self._logger.warning("Resetting sensor due to overflow.")
                    return self.error
                self.data["values"]["volumeflow"] = {
                    "value": flow,
                    "unit": self._units["volumeflow"],
                }
                self.data["error"] = False
                self._logger.debug("Reading successful: %s", flow)
                return self.data
            else:
                self.mux.close_all_ports()
                self.error = Error().crc(self)
                return self.error
        else:
            self.mux.close_all_ports()
            self.error = Error().read(self)
            return self.error


class SFMXXX(SFM):
    """ Deprecated class identifier. Use SFM instead."""
    pass


class SFM3XXX(SFM):
    """ Deprecated class identifier. Use SFM instead."""
    pass

