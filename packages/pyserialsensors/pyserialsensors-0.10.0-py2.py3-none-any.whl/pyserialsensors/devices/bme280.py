# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
Sensor Class for BME280
based on
https://github.com/adafruit/Adafruit_Python_BME280
Copyright (c) 2014 Adafruit Industries
Author: Tony DiCola
Based on the BMP280 driver with BME280 changes provided by
David J Taylor, Edinburgh (www.satsignal.eu). Additional functions added
by Tom Nardi (www.ifail.com)
"""

__author__ = "Konstantin Niehaus"
__copyright__ = "German Aerospace Center"
__credits__ = ["Konstantin Niehaus"]
__license__ = "MIT"
__version__ = "0.1.0"
__email__ = "konstantin.niehaus@dlr.de"

import time
from ..core.error import Error
from ..core.sensor import I2CSensor

import logging

logging.basicConfig(level=logging.DEBUG)


class BME280(I2CSensor):
    """
    Reads absolute pressure [Pa], humidity [pct] and temperature [°C]
    """

    __name__ = "BME280"

    _units = {
        "abs_pressure": "Pa",
        "humidity": "pct",
        "temperature": "C",
    }

    # BME280 default address.
    _SENSOR_ADDRESS = 0x77
    _MODE_SLEEP = 0x00
    _MODE_FORCE = 0x01
    _MODE_NORMAL = 0x03

    # Maximum clock frequency [Hz]
    _i2c_freq = 4e5
    _delay = 2e-2

    # Operating Modes
    __OSAMPLE_1 = 1
    __OSAMPLE_2 = 2
    __OSAMPLE_4 = 3
    __OSAMPLE_8 = 4
    __OSAMPLE_16 = 5

    # Standby Settings
    __STANDBY_0p5 = 0
    __STANDBY_62p5 = 1
    __STANDBY_125 = 2
    __STANDBY_250 = 3
    __STANDBY_500 = 4
    __STANDBY_1000 = 5
    __STANDBY_10 = 6
    __STANDBY_20 = 7

    # Filter Settings
    __FILTER_off = 0
    __FILTER_2 = 1
    __FILTER_4 = 2
    __FILTER_8 = 3
    __FILTER_16 = 4

    # Trimming parameter registers
    _REG_T1_LSB = 0x88
    _REG_T1_MSB = 0x89
    _REG_T2_LSB = 0x8A
    _REG_T2_MSB = 0x8B
    _REG_T3_LSB = 0x8C
    _REG_T3_MSB = 0x8D

    _REG_P1_LSB = 0x8E
    _REG_P1_MSB = 0x8F
    _REG_P2_LSB = 0x90
    _REG_P2_MSB = 0x91
    _REG_P3_LSB = 0x92
    _REG_P3_MSB = 0x93
    _REG_P4_LSB = 0x94
    _REG_P4_MSB = 0x95
    _REG_P5_LSB = 0x96
    _REG_P5_MSB = 0x97
    _REG_P6_LSB = 0x98
    _REG_P6_MSB = 0x99
    _REG_P7_LSB = 0x9A
    _REG_P7_MSB = 0x9B
    _REG_P8_LSB = 0x9C
    _REG_P8_MSB = 0x9D
    _REG_P9_LSB = 0x9E
    _REG_P9_MSB = 0x9F

    _REG_H1 = 0xA1
    _REG_H2_LSB = 0xE1
    _REG_H2_MSB = 0xE2
    _REG_H3 = 0xE3
    _REG_H4_LSB = 0xE5
    _REG_H4_MSB = 0xE4
    _REG_H5_LSB = 0xE5
    _REG_H5_MSB = 0xE6
    _REG_H6 = 0xE7

    _REG_CHIPID = 0xD0
    _REG_VERSION = 0xD1
    _REG_SOFTRESET = 0xE0

    _REG_STATUS = 0xF3
    _REG_CONTROL_HUM = 0xF2
    _REG_CONTROL = 0xF4
    _REG_CONFIG = 0xF5
    _REG_DATA = 0xF7

    t1, t2, t3 = [None] * 3

    p1, p2, p3 = [None] * 3
    p4, p5, p6 = [None] * 3
    p7, p8, p9 = [None] * 3

    h1, h2, h3 = [None] * 3
    h4, h5, h6 = [None] * 3

    t_fine = 0.0

    def __init__(
        self,
        *args,
        t_mode: int = __OSAMPLE_1,
        p_mode: int = __OSAMPLE_16,
        h_mode: int = __OSAMPLE_1,
        standby: int = __STANDBY_250,
        _filter: int = __FILTER_off,
        **kwargs
    ) -> None:
        """
        Initialize mode configration

        Args:
            t_mode (int): Temperature mode (defaults to 1)
            p_mode (int): Pressure mode (defaults to 5)
            h_mode (int): Humidity mode (defaults to 1)
            standby (int): Standby duration (defaults to 3 (250ms))
            filter (int): IIR filter (defaults to off - 0)
        """

        super().__init__(*args, **kwargs)

        # Check arguments
        ## Check that p_mode is valid.
        if p_mode not in [
            self.__OSAMPLE_1,
            self.__OSAMPLE_2,
            self.__OSAMPLE_4,
            self.__OSAMPLE_8,
            self.__OSAMPLE_16,
        ]:
            raise ValueError("Unexpected p_mode value {0}.".format(p_mode))

        ## Check that h_mode is valid.
        if h_mode not in [
            self.__OSAMPLE_1,
            self.__OSAMPLE_2,
            self.__OSAMPLE_4,
            self.__OSAMPLE_8,
            self.__OSAMPLE_16,
        ]:
            raise ValueError("Unexpected h_mode value {0}.".format(h_mode))

        ## Check that standby is valid.
        if standby not in [
            self.__STANDBY_0p5,
            self.__STANDBY_62p5,
            self.__STANDBY_125,
            self.__STANDBY_250,
            self.__STANDBY_500,
            self.__STANDBY_1000,
            self.__STANDBY_10,
            self.__STANDBY_20,
        ]:
            raise ValueError("Unexpected standby value {0}.".format(standby))

        ## Check that filter is valid.
        if _filter not in [
            self.__FILTER_off,
            self.__FILTER_2,
            self.__FILTER_4,
            self.__FILTER_8,
            self.__FILTER_16,
        ]:
            raise ValueError("Unexpected filter value {0}.".format(_filter))

        self._p_mode = p_mode
        self._t_mode = t_mode
        self._h_mode = h_mode
        self._standby = standby
        self._filter = _filter

        self.param_t1 = None
        self.param_t2 = None
        self.param_t3 = None

        self.param_p1 = None
        self.param_p2 = None
        self.param_p3 = None
        self.param_p2 = None
        self.param_p3 = None
        self.param_p4 = None
        self.param_p5 = None
        self.param_p6 = None
        self.param_p7 = None
        self.param_p8 = None
        self.param_p9 = None

        self.param_h1 = None
        self.param_h2 = None
        self.param_h3 = None
        self.param_h4 = None
        self.param_h5 = None
        self.param_h6 = None

        self._logger.debug("Init")
        self.reset()
        self.exists = self.sensor_exists()

    def get_serial_number(self) -> str:
        """
        A serial number is not supported by bme280
        hence a pseudo identifier is calculated by
        adding the individual calibration values together

        Returns:
            str: Serial number information or None
        """

        serial_number = 0
        for i in range(self._REG_T1_MSB, self._REG_H6)[:10]:
            calib_parameter = self.getU8(i)

            if calib_parameter is not None:
                serial_number += calib_parameter
            else:
                serial_number = None
                break

        if serial_number is not None:
            self.serial_number = serial_number
            self._logger.info("Assigned pseudo-serial number %s", serial_number)
        return serial_number

    def reset(self) -> None:
        """
        Reset sensor to default.
        """

        self._logger.debug("Resetting...")
        self.txrx(self._REG_SOFTRESET, readlen=2)
        self._logger.debug("Done resetting...")

    def init(self) -> None:
        """
        Initialize sensor communication
        * Activate sleep mode
        * Write filter and standby calibration
        * Write humidty oversampling rate
        * Write temperature oversampling rate
        * Write pressure oversampling rate
        """
        # Sleep mode
        self.txrx([self._REG_CONTROL, 0x24], readlen=0)
        time.sleep(self._delay)

        # Setup filter and standby
        cmd = (self._standby << 5) | (self._filter << 2)
        self.txrx([self._REG_CONFIG, cmd], readlen=0)
        time.sleep(self._delay)

        # Set humidity oversampling
        self.txrx([self._REG_CONTROL_HUM, self._h_mode], readlen=0)

        # Set Temp/Pressure Oversample and enter Normal mode
        cmd = (self._t_mode << 5) + (self._p_mode << 2) + self._MODE_NORMAL

        self.txrx([self._REG_CONTROL, cmd], readlen=0)

    def sensor_exists(self) -> bool:
        """
        Test if sensor is plugged in and works proper

        Returns:
            bool: True if test was successful, otherwise False.
        """

        # Check if sensor is responsive
        serial_number = self.get_serial_number()
        self._logger.info("Pseudo serial number %s", serial_number)

        if isinstance(serial_number, int):
            # Prepare measurement
            self.prepare_measurement()
            self.exists = True
        else:
            self.error = Error().read(self)
            self.exists = False
        return self.exists

    def load_calibration(self) -> bool:
        """
        Load all calibration data needed for the calculation of
        Temperature, Humidtiy and absolute pressure.

        Returns:
            bool: True if read has been completed successfully, False otherwise.
        """

        self.param_t1 = self.getU16(self._REG_T1_MSB, self._REG_T1_LSB)
        if self.param_t1 is None:
            return False

        self.param_t2 = self.getS16(self._REG_T2_MSB, self._REG_T2_LSB)
        self.param_t3 = self.getS16(self._REG_T3_MSB, self._REG_T3_LSB)

        self.param_p1 = self.getU16(self._REG_P1_MSB, self._REG_P1_LSB)
        self.param_p2 = self.getS16(self._REG_P2_MSB, self._REG_P2_LSB)
        self.param_p3 = self.getS16(self._REG_P3_MSB, self._REG_P3_LSB)
        self.param_p4 = self.getS16(self._REG_P4_MSB, self._REG_P4_LSB)
        self.param_p5 = self.getS16(self._REG_P5_MSB, self._REG_P5_LSB)
        self.param_p6 = self.getS16(self._REG_P6_MSB, self._REG_P6_LSB)
        self.param_p7 = self.getS16(self._REG_P7_MSB, self._REG_P7_LSB)
        self.param_p8 = self.getS16(self._REG_P8_MSB, self._REG_P8_LSB)
        self.param_p9 = self.getS16(self._REG_P9_MSB, self._REG_P9_LSB)

        self.param_h1 = self.getU8(self._REG_H1)
        self.param_h2 = self.getS16(self._REG_H2_MSB, self._REG_H2_LSB)
        self.param_h3 = self.getU8(self._REG_H3)
        self.param_h4 = (self.getU8(self._REG_H4_MSB) << 4) + (
            self.getU8(self._REG_H4_LSB) & 0x0F
        )
        self.param_h5 = (self.getU8(self._REG_H5_MSB) << 4) + (
            (self.getU8(self._REG_H5_LSB) >> 4) & 0x0F
        )
        self.param_h6 = self.getS8(self._REG_H6)

        self._logger.debug("t1 = %s", self.param_t1)
        self._logger.debug("t2 = %s", self.param_t2)
        self._logger.debug("t3 = %s", self.param_t3)

        self._logger.debug("p1 = %s", self.param_p1)
        self._logger.debug("p2 = %s", self.param_p2)
        self._logger.debug("p3 = %s", self.param_p3)
        self._logger.debug("p4 = %s", self.param_p4)
        self._logger.debug("p5 = %s", self.param_p5)
        self._logger.debug("p6 = %s", self.param_p6)
        self._logger.debug("p7 = %s", self.param_p7)
        self._logger.debug("p8 = %s", self.param_p8)
        self._logger.debug("p9 = %s", self.param_p9)

        self._logger.debug("h1 = %s", self.param_h1)
        self._logger.debug("h2 = %s", self.param_h2)
        self._logger.debug("h3 = %s", self.param_h3)
        self._logger.debug("h4 = %s", self.param_h4)
        self._logger.debug("h5 = %s", self.param_h5)
        self._logger.debug("h6 = %s", self.param_h6)

        return True

    def prepare_measurement(self) -> bool:
        """
        Placeholder function to be compatible with other sensor classes

        Returns:
            bool: True if test was successful, otherwise False.
        """

        if self.load_calibration():
            self.init()
            return True
        else:
            return False

    def get_data(self) -> dict:
        """
        Get current measurement values

        Returns:
            dict: Data dictionary
        """

        # Wait until data is ready
        if self.error is not None:
            res = self.prepare_measurement()
            if res:
                self.error = None
            else:
                self.error = Error().read(self)
                self.reset()
                self.prepare_measurement()
                self.data["object"] = "ERROR"
                return self.data

        self.data = self.default_data()
        raw_data = None
        try:
            raw_data = self.get_raw_data()
        except TypeError:
            # Throw an error if not able to fetch data
            self.error = Error().read(self)
            self.reset()
            self.prepare_measurement()
            self.data["object"] = "ERROR"
            return self.data

        if raw_data is None:
            # Throw an error if not able to fetch data
            self.error = Error().read(self)
            self.data["object"] = "ERROR"
            return self.data

        if self.error is None:
            temperature = self.read_temperature(raw_data)
            if temperature is not None:
                temperature = round(temperature, 3)
            else:
                # Throw an error if not able to fetch data
                self.error = Error().read(self)
                self.data["object"] = "ERROR"
                return self.data

            pressure = int(self.read_pressure(raw_data))
            humidity = round(self.read_humidity(raw_data), 3)
            self.data["error"] = False
            self.data["values"] = {}
            self.data["values"]["abs_pressure"] = {
                "value": pressure,
                "unit": self._units["abs_pressure"],
            }
            self.data["values"]["temperature"] = {
                "value": temperature,
                "unit": self._units["temperature"],
            }
            self.data["values"]["humidity"] = {
                "value": humidity,
                "unit": self._units["humidity"],
            }

        return self.data

    def get_raw_data(self) -> bytearray:
        """
        Read all values from devices needed to calculate
        humidity, pressure and temperature values

        Returns:
            bytearray: Raw data array
        """

        i = 0
        while i < self._max_attempts:
            state = self.getU8([self._REG_STATUS])
            if state is not None and state & 0x08:
                time.sleep(self._delay)
            elif state is None:
                return None
            i += 1
        return self.txrx([self._REG_DATA], 8)

    @classmethod
    def read_raw_temp(cls, raw_data: bytearray) -> int:
        """
        Calculate uncompensated raw temperature from sensor.

        Returns:
            int: Raw adc read
        """

        raw = (raw_data[3] << 16) | (raw_data[4] << 8) | (raw_data[5])
        raw >>= 4
        return raw

    @classmethod
    def read_raw_pressure(cls, raw_data: bytearray) -> int:
        """
        Calculate raw (uncompensated) pressure level from the sensor.

        Returns:
            int: Raw adc read
        """

        raw = (raw_data[0] << 12) | (raw_data[1] << 4) | (raw_data[2] >> 4 & 0x0F)
        return raw

    @classmethod
    def read_raw_humidity(cls, raw_data: bytearray) -> int:
        """
        Calculate raw (uncompensated) humidity value from the sensor.

        Args:
            raw_data (bytearray): Full raw data array (temperature,pressure and humidity)

        Returns:
            int: Raw adc read
        """

        raw = (raw_data[6] << 8) | raw_data[7]
        if raw is not None and raw is int:
            if raw > 32767:
                raw -= 65536
        return raw

    def read_temperature(self, raw_data: bytearray) -> float:
        """
        Convert raw temperature to compensated temperature in °C

        Args:
            raw_data (bytearray): Full raw data array (temperature,pressure and humidity)

        Returns:
            float: Temperature in °C or None if conversion failed
        """

        adc = self.read_raw_temp(raw_data)
        self._logger.debug("Temperature raw data %s", adc)

        if adc is None:
            self._logger.error("Temperature data not valid.")
        elif None not in [self.param_t1, self.param_t2, self.param_t3]:
            var1 = (adc / 16384.0 - self.param_t1 / 1024.0) * self.param_t2
            var2 = ((adc / 131072.0 - self.param_t1 / 8192.0) ** 2) * self.param_t3
            self.t_fine = var1 + var2
            return self.t_fine / 5120.0

        else:
            self._logger.error("Calibration data not available.")
        return None

    def read_pressure(self, raw_data: bytearray) -> float:
        """
        Convert raw pressure to compensated pressure in Pa

        Args:
            raw_data (bytearray): Full raw data array (temperature,pressure and humidity)

        Returns:
            float: Pressure in Pa
        """

        adc = self.read_raw_pressure(raw_data)
        self._logger.debug("Pressure raw data %s", adc)

        var1 = float(self.t_fine) / 2.0 - 64000.0
        var2 = var1 * var1 * float(self.param_p6) / 32768.0
        var2 = var2 + var1 * float(self.param_p5) * 2.0
        var2 = var2 / 4.0 + float(self.param_p4) * 65536.0
        var1 = (
            float(self.param_p3) * var1 * var1 / 524288.0 + float(self.param_p2) * var1
        ) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * float(self.param_p1)
        if var1 == 0:
            return 0
        abs_p = 1048576.0 - adc
        abs_p = ((abs_p - var2 / 4096.0) * 6250.0) / var1
        var1 = float(self.param_p9) * abs_p * abs_p / 2147483648.0
        var2 = abs_p * float(self.param_p8) / 32768.0
        abs_p = abs_p + (var1 + var2 + float(self.param_p7)) / 16.0
        return abs_p

    def read_humidity(self, raw_data: bytearray) -> float:
        """
        Convert raw rel. humidity to compensated relative humidity in %

        Args:
            raw_data (bytearray): Full raw data array (temperature,pressure and humidity)

        Returns:
            float: Relative humidity in %
        """

        adc = self.read_raw_humidity(raw_data)
        self._logger.debug("Humidity raw data %s", adc)

        # Algorithm from the BME280 driver
        # https://github.com/BoschSensortec/BME280_driver/blob/master/bme280.c
        var1 = float(self.t_fine) - 76800.0
        var2 = self.param_h4 * 64.0 + (self.param_h5 / 16384.0) * var1
        var3 = adc - var2
        var4 = self.param_h2 / 65536.0
        var5 = 1.0 + (self.param_h3 / 67108864.0) * var1
        var6 = 1.0 + (self.param_h6 / 67108864.0) * var1 * var5
        var6 = var3 * var4 * var5 * var6
        res = var6 * (1.0 - self.param_h1 * var6 / 524288.0)
        humidity = max(0.0, min(res, 100.0))
        return humidity

    def read_dewpoint(self, raw_data: bytearray) -> float:
        """
        Return calculated dewpoint in °C, only accurate at > 50% RH
        """
        celsius = self.read_temperature(raw_data)
        humidity = self.read_humidity(raw_data)
        dewpoint = celsius - ((100 - humidity) / 5)
        return dewpoint

    def read_dewpoint_f(self, raw_data: bytearray) -> float:
        """
        Calculated dewpoint in F, only accurate at > 50% RH
        """
        dewpoint_c = self.read_dewpoint(raw_data)
        dewpoint_f = dewpoint_c * 1.8 + 32
        return dewpoint_f
