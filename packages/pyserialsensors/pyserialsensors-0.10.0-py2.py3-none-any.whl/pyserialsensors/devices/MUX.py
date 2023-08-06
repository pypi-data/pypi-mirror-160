# SPDX-FileCopyrightText: 2022 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
    Module for I2C Multplexers

    Supported MUX:
      + TCA9548A
      + PCA9548A
"""

import time
from pyftdi.i2c import I2cNackError, I2cIOError
import logging


class TCA9548:
    """
    Driver for TCA9548A 8 port I2C multiplexer
    """

    # Supported adress space
    MUX_ADDRESS_LIST = range(0x70, 0x77 + 1)
    # Port adresses
    MUX_PORT_LIST = range(8)
    # Device delay
    __DELAY = 0.001
    # Maximum number of communication attempts
    __MAX_ATTEMPTS = 10

    def __init__(
        self,
        bus: "core.i2controller.I2cController",
        addr: int,
        loglvl: int = logging.INFO,
        **kwargs,
    ):
        """
        Args:
            bus (core.I2cController): Associated I2C bus
            addr (int): MUX I2C address
            loglvl (int): Loglevel (see logging module)
        """

        self.bus = bus
        self.address = addr
        self._state = None
        if self.address and bus:
            self._logger = logging.getLogger(str(self))
            self._logger.setLevel(loglvl)

    def __str__(self) -> str:
        if self.address:
            return f"MUX{self.address:02x}@{self.bus.ftdi._usb_dev.serial_number}"
        return f"No address assigned"

    def connected(self) -> bool:
        """
        Check if something is listening on the given address

        Returns:
            bool: True if connected, false otherwise
        """
        for i in range(3):
            self._logger.debug(f"Polling")
            try:
                if self.bus.poll(self.address):
                    # Test the connected device by trying to close all
                    state = self.get_state()
                    self.close_all_ports()
                    # Check state
                    state = self.get_state()
                    if state == 0:
                        self._logger.debug(f"Connected")
                        return True
            except (I2cNackError, I2cIOError):
                pass
        return False

    def get_state(self) -> bytearray:
        """
        Get status of all MUX-ports

        Returns:
            bytearray: Binary coded state array
        """

        msg = None
        try:
            msg = self.bus.read(self.address)[0]
        except (I2cIOError, I2cNackError):
            pass
        return msg

    def open_port(self, Port) -> bytearray:
        # Check if only on port is requested to be opened
        if type(Port) is int:
            Port = [Port]
        elif type(Port) is not list:
            raise TypeError("Port type is {type(Port)} only int and list supported")

        # Get current port states
        cmd = self.get_state()

        # Modify state if additional ports
        # were requested to be opened
        for port in Port:
            cmd = cmd | (1 << port)

        # Apply changes
        self.write(cmd)
        return cmd

    def open_single_port(self, port: int) -> bytearray:
        """
        Open a single port

        Returns:
            bytearray: Binary coded state array
        """

        cmd = 1 << port
        self._state = self.get_state()

        if cmd != self._state:
            self.write(cmd)
            state = self.get_state()
            if state == 2**port:
                self._logger.debug("Successfully opened port %s only.", port)
            else:
                self._logger.warning("Failed to open %s.", port)

            self._state = state
        return self._state

    def write(self, cmd: bytearray) -> bytearray:
        """
        Write data to MUX

        Args:
            cmd (bytearray): MUX command

        Returns:
            bytearray: Returns False if communication failed or bytearray
            of return values
        """

        attempt = 0
        while attempt < self.__MAX_ATTEMPTS:
            try:
                if isinstance(cmd, list):
                    self.bus.write(self.address, cmd)
                else:
                    self.bus.write(self.address, [cmd])

                time.sleep(self.__DELAY)
                return cmd
            except (I2cNackError, I2cIOError):
                attempt += 1
        return False

    def poll(self, addr: int) -> bool:
        """
        Poll I2C address

        Args:
            addr (int): Device poll address

        Returns:
            bool: True if a device anserwed, false otherwise.
        """

        attempt = 0
        while attempt < self.__MAX_ATTEMPTS:
            try:
                found = self.bus.poll(addr, write=True)
                if found:
                    self._logger.info(f"Found device @{addr:02x}h")
                return found
            except (I2cNackError, I2cIOError):
                attempt += 1
        return False

    def is_open(self, port: int) -> bool:
        """
        Check if specific mux port is open

        Returns:
            bool: True if port is open, false otherwise.
        """

        state = self.get_state()
        if (state & (1 << port)) >> port == 0:
            return False
        return True

    def send(self, port: int, addr: int, cmd: bytearray) -> bool:
        """
        Sending command to a device connected to a specific port.

        Args:
            port (int): Multiplexer port number (0<port<8)
            addr (int): device address
            cmd (bytearray): Command that shall be send to connected device

        Returns:
            bool: True if sending was successful, false otherwise.
        """

        self.open_single_port(port)
        try:
            self.byte_logger(cmd, port, addr)
            self.bus.write(addr, cmd)
            time.sleep(self.__DELAY)
            return True
        except (I2cNackError, I2cIOError):
            self.close_all_ports()
            return False

    def byte_logger(
        self, cmd: bytearray, port: int, addr: int, sep: str = "->"
    ) -> None:
        """
        Write IO data to logger

        Args:
            cmd (bytearray): Command that shall be send to connected device
            port (int): Multiplexer port number (0<port<8)
            addr (int): device address
            sep (str): Separator in text message (default "->")

        """

        log_str = "["
        if cmd is not None and len(cmd) > 0:
            log_str += f"{cmd[0]:02x}"
            if len(cmd) > 1:
                for c in cmd[1:]:
                    log_str += f" {c:02x}"
        log_str += f"] {sep} {addr:02x}@{port}"
        self._logger.debug(log_str)

    def exchange(
        self, addr: int, port: int, cmd: bytearray, readlength: int = 1
    ) -> bytearray:
        """
        Exchanging data with the sensor

        Args:
            port (int): Multiplexer port number (0<port<8)
            addr (int): Device address
            cmd (bytearray): Command that shall be send to connected device
            readlength (int): Expected length of the received data}

        :return: [BYTEARRAY] data if exchange is successful else None
        """
        if isinstance(cmd, int):
            cmd = [cmd]
        elif not isinstance(cmd, list):
            raise AttributeError(f"Expected int or list not {type(cmd)}")

        self.open_single_port(port)
        state = self.send(port, addr, cmd)

        self._logger.debug(f"{cmd} -> {addr:02x}h")
        if not state:
            data = None
            self._logger.error("Failed to write %s to %s@%s", cmd, port, addr)
        else:
            data = self.receive(addr, port, readlength=readlength)
        return data

    def receive(self, addr: int, port: int, readlength: int = 1) -> bytearray:
        """
        Reading data from sensor

        Args:
            port (int): Multiplexer port number (0<port<8)
            addr (int): Device address
            cmd (bytearray): Command that shall be send to connected device
            readlength (int): Expected length of the received data}

        Returns:
            bytearray: data if exchange is successful else None

        """

        self.open_single_port(port)

        try:
            ba = self.bus.read(addr, readlen=readlength)
            self.byte_logger(ba, port, addr, sep="<-")
            time.sleep(self.__DELAY)
            self._logger.debug(f"{addr:02x}h -> {ba}")
            return ba
        except (I2cNackError, I2cIOError):
            self._logger.error("Failed to read from %s@%s", port, addr)
            self.close_all_ports()
            return None

    def close_all_ports(self) -> bool:
        """
        Closing all ports on the multiplexer.
        This is necessary if more than one multiplexer is used.

        Returns:
            bool: True if ports are closed successfully else False
        """

        self.bus.write(self.address, [0x00])
        self.state = 0
        time.sleep(self.__DELAY)
