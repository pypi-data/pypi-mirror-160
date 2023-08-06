# -*- coding: utf-8 -*-
# Copyright (C) 2022 Paul Grebeniuk <paul@coolautomation.com>

# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 2.1 of the License, or (at your
# option) any later version.

# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

"""
    sub20.Device
    =====================
    Device class implementation of :mod:`sub20`.
    .. moduleauthor::  Paul Grebeniuk  <paul@coolautomation.com>
"""

import sys
from ctypes import create_string_buffer, c_int

from sub20.ctypeslib.libsub import SIGNATURES, sub_version
from sub20.ctypeslib.utils import load_ctypes_library
from sub20._errors import SubDeviceError, SubNotFoundError, SubNotOpenedError

# Enum

""" RS232/RS485"""
RS_RX_ENABLE = 0x80
RS_TX_ENABLE = 0x40

# Character Size
RS_CHAR_5 = 0x00
RS_CHAR_6 = 0x02
RS_CHAR_7 = 0x04
RS_CHAR_8 = 0x06
RS_CHAR_9 = 0x07

# Parity
RS_PARITY_NONE = 0x00
RS_PARITY_EVEN = 0x20
RS_PARITY_ODD = 0x30

# Stop Bits
RS_STOP_1 = 0x00
RS_STOP_2 = 0x08

# Timing Flags
RS_RX_BEFORE_TX = 0x01
RS_RX_AFTER_TX = 0x02

FIFO_SELECT_UART = 0x02

I2C_GCE = 0x01
I2C_DISABLE = 0x02

MAX_BUF_SZ = 64
MAX_FREQ = 444444


class SUBDevice(object):

    def __init__(self, buffer_size=MAX_BUF_SZ):
        libname = 'sub20.dll' if sys.platform == "win32" \
            else 'libsub.so'

        self._libsub = load_ctypes_library(libname, SIGNATURES)
        self.sub_errno = c_int.in_dll(self._libsub, "sub_errno")
        self.sub_i2c_status = c_int.in_dll(self._libsub, "sub_i2c_status")
        self._device = None
        self.rx_buf_sz = buffer_size
        self.rx_buf = create_string_buffer(buffer_size)

    def open(self):
        self._device = self._libsub.sub_open(None)
        if not self._device:
            raise SubNotFoundError()

    def sub_get_serial_number(self):
        """
        Get serial number of SUB-20 device
        :returns: The serial number string
        :rtype: str
        :raises SubNotOpenedError:  if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code

        """

        if not self._device:
            raise SubNotOpenedError()
        rx_buf_sz = MAX_BUF_SZ
        rx_buf = create_string_buffer(rx_buf_sz)
        if self._libsub.sub_get_serial_number(self._device, rx_buf, rx_buf_sz):
            raise SubDeviceError(self.exc_str())
        return rx_buf.value.decode('UTF-8')

    def sub_get_product_id(self):
        """
       Get product ID of SUB-20 device
       :returns: The product ID string
       :rtype: str
       :raises SubNotOpenedError:  if the device is not opened
       :raises SubDeviceError: if the wrapped function returned the error code

       """
        if not self._device:
            raise SubNotOpenedError()
        rx_buf_sz = MAX_BUF_SZ
        rx_buf = create_string_buffer(rx_buf_sz)
        if self._libsub.sub_get_product_id(self._device, rx_buf, rx_buf_sz):
            raise SubDeviceError(self.exc_str())
        return rx_buf.value.decode('UTF-8')

    def sub_get_version(self):
        """
      Get version of the sub20 library, driver and SUB-20 firmware
      :returns: The pointer to the sub20 inner version structure
      :rtype: c_void_p
      :raises SubNotOpenedError:  if the device is not opened

      """
        if not self._device:
            raise SubNotOpenedError()
        return sub_version.from_address(self._libsub.sub_get_version(self._device))

    def sub_get_version_dict(self):
        """
        Get the version in the python dictionary
        :returns: The pointer to the sub20 inner version structure
        :rtype: dict

        """
        version = self.sub_get_version()
        return {"dll": f'{version.dll.major}.{version.dll.minor}.'
                       f'{version.dll.micro}.{version.dll.nano}',
                "driver": f'{version.driver.major}.{version.driver.minor}.'
                          f'{version.driver.micro}.{version.driver.nano}',
                "sub_device": f'{version.sub_device.major}.{version.sub_device.minor}.'
                              f'{version.sub_device.micro}.{version.sub_device.nano}'
                }

    def sub_reset(self):
        if not self._device:
            raise SubNotOpenedError()
        if self._libsub.sub_reset(self._device):
            raise SubDeviceError(self.exc_str())

    def sub_eep_read(self, addr, sz=MAX_BUF_SZ):
        """
        Read sz bytes (no more than 64(default value)) from internal EEPROM starting from the given address
        :param addr: The start address
        :type addr: int
        :param sz:
        :type sz: int
        :returns: buffer
        :rtype: bytes
        :raises SubNotOpenedError:  if the device is not opened
        :raises ValueError:  if sz > 64
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()

        if sz > MAX_BUF_SZ:
            raise ValueError("Maximal buffer size exceeded!")

        if self._libsub.sub_eep_read(self._device, addr, self.rx_buf, sz):
            raise SubDeviceError(self.exc_str())

        return self.rx_buf

    def sub_eep_write(self, addr, data: bytes):
        """
        Write data (with size no more than 64 bytes) to internal EEPROM starting from the given address
        :param addr: The start address
        :type addr: int
        :param data:
        :type data: int
        :raises SubNotOpenedError:  if the device is not opened
        :raises ValueError:  if len(data) > 64
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()
        tx_buf_sz = len(data)
        if tx_buf_sz > MAX_BUF_SZ:
            raise ValueError("Maximal buffer size exceeded!")
        tx_buf = create_string_buffer(data)
        if self._libsub.sub_eep_write(self._device, addr, tx_buf, tx_buf_sz):
            raise SubDeviceError(self.exc_str())

    def sub_i2c_freq(self, freq=0):
        """
        Set and get SUB-20 I2C master clock frequency.
        :param freq: a frequency. if freq == 0 it's a get function otherwise it's a set function
        :type freq: int
        :returns: a current frequency if freq == 0 otherwise it just returns freq value
        :rtype: int
        :raises SubNotOpenedError:  if the device is not opened
        :raises ValueError:  freq > 444444
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()

        if freq > MAX_FREQ:
            raise ValueError("Maximal frequency exceeded!")

        _freq = c_int(freq)
        if self._libsub.sub_i2c_freq(self._device, _freq):
            raise SubDeviceError(self.exc_str())

        return _freq.value

    def sub_i2c_config(self, sa, flags):
        """
        Configure SUB-20 I2C module.

        :param sa: slave address for SUB-20 in I2C slave mode
        :type sa: int
        :param flags: I2C_GCE | I2C_DISABLE
        :type flags: int
        :raises SubNotOpenedError:  if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code

        """

        if not self._device:
            raise SubNotOpenedError()

        if self._libsub.sub_i2c_freq(self._device, sa, flags):
            raise SubDeviceError(self.exc_str())

    def sub_i2c_start(self):
        if not self._device:
            raise SubNotOpenedError()

        if self._libsub.sub_i2c_start(self._device):
            raise SubDeviceError(self.exc_str())

    def sub_i2c_stop(self):
        if not self._device:
            raise SubNotOpenedError()

        if self._libsub.sub_i2c_stop(self._device):
            raise SubDeviceError(self.exc_str())

    def sub_i2c_scan(self):
        """
        Scan I2C bus looking for connected slave devices.

        :returns: List of available i2c addresses
        :rtype: list
        :raises SubNotOpenedError:  if the device is not opened

        """
        if not self._device:
            raise SubNotOpenedError()
        addresses = []

        counter = c_int(1)
        rc = self._libsub.sub_i2c_scan(self._device, counter, self.rx_buf)
        if not rc:
            for ii in range(0, counter.value):
                addresses.append(ord(self.rx_buf[ii]))
        return addresses

    def sub_i2c_read(self, sa, ma, ma_sz, rx_buf_sz):
        """
        I2C master read transaction.

        :param sa: slave address for SUB-20 in I2C slave mode
        :type sa: int
        :param ma: memory address
        :type ma: int
        :param ma_sz: memory address size bytes
        :type ma: int
        :param rx_buf_sz: read data size bytes
        :type rx_buf_sz: int
        :returns: rx buffer
        :rtype: bytes
        :raises SubNotOpenedError:  if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()

        rx_buf = create_string_buffer(rx_buf_sz)
        _rc = self._libsub.sub_i2c_read(self._device, sa, ma, ma_sz, rx_buf, rx_buf_sz)
        if _rc:
            raise SubDeviceError(self.exc_str())
        return self.rx_buf

    def sub_i2c_write(self, sa, ma, ma_sz, data_buf, data_buf_sz):
        """
        I2C master write transaction.

        :param sa: slave address for SUB-20 in I2C slave mode
        :param ma: memory address
        :param ma_sz: memory address size
        :param data_buf: buffer for data to be written
        :param data_buf_sz: data buffer size in bytes
        :type data_buf: bytes
        :type sa: int
        :type ma: int
        :type ma_sz: int
        :type data_buf_sz: int
        :raises SubNotOpenedError:  if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()
        if self._libsub.sub_i2c_read(self._device, sa, ma, ma_sz, data_buf, data_buf_sz):
            raise SubDeviceError(self.exc_str())

    def sub_i2c_transfer(self, sa, data_buf, data_size, rx_buf_sz):
        """
        I2C master write transaction followed by master read transaction.

        :param sa: slave address for SUB-20 in I2C slave mode
        :type sa: int
        :param data_buf: memory address
        :type data_buf: int
        :param data_size: memory address size
        :type data_size: int
        :param rx_buf_sz: rx buffer size in bytes
        :type rx_buf_sz: int
        :returns: rx buffer
        :rtype: bytes
        :raises SubNotOpenedError:  if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()
        rx_buf = create_string_buffer(rx_buf_sz)

        if self._libsub.sub_i2c_transfer(self._device, sa, data_buf, data_size, rx_buf, rx_buf_sz):
            raise SubDeviceError(self.exc_str())

        return rx_buf

    def sub_gpio_config(self, set_par: int, mask: int):
        """
        Configure GPIO state (direction) as input or output.
        :param set_par: Bits 0-31 of set parameter correspond to GPIO0-GPIO31 configuration bits. If GPIOn configuration bit is "1" then GPIOn direction is output, otherwise it is input.
        :param mask: Bit in set parameter will take effect only if corresponding mask bit is "1". With mask=0 function will only read current GPIO configuration.
        :returns: current GPIO configuration state
        :rtype: int32
        :raises SubNotOpenedError:  if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()
        get_par = c_int(1)
        _rc = self._libsub.sub_gpio_config(self._device, set_par, get_par, mask)
        if _rc:
            raise SubDeviceError(self.exc_str())
        return get_par.value

    def sub_gpio_read(self):
        """
        Read GPIO input status
        :returns: received GPIO input status
        :rtype: int32
        :raises SubNotOpenedError:  if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()
        get_par = c_int(1)
        _rc = self._libsub.sub_gpio_read(self._device, get_par)
        if _rc:
            raise SubDeviceError(self.exc_str())
        return get_par.value

    def sub_gpio_write(self, set_par, mask):
        """
        Set GPIO output status

        :param set_par: Bits 0-31 of set parameter correspond to GPIO0-GPIO31 output statuses.
        :param mask: Bit in set parameter will take effect only if corresponding mask bit is "1". With mask=0 function will only read current GPIO output status.
        :returns: received GPIO output status.
        :rtype: int32
        :raises SubNotOpenedError:  if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()
        get_par = c_int(1)
        _rc = self._libsub.sub_gpio_write(self._device, set_par, get_par, mask)
        if _rc:
            raise SubDeviceError(self.exc_str())
        return get_par.value

    def sub_gpiob_config(self, set_par: int, mask: int):

        """
        Configure GPIOB state (direction) as input or output.

        :param set_par: Bits 0-31 of set parameter correspond to GPIO0-GPIO31 configuration bits. If GPIOn configuration bit is "1" then GPIOn direction is output, otherwise it is input.
        :param mask: Bit in set parameter will take effect only if corresponding mask bit is "1". With mask=0 function will only read current GPIO configuration.
        :returns: current GPIO configuration state
        :rtype: int32
        :raises SubNotOpenedError:  if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()
        get_par = c_int(1)
        _rc = self._libsub.sub_gpiob_config(self._device, set_par, get_par, mask)
        if _rc:
            raise SubDeviceError(self.exc_str())
        return get_par.value

    def sub_gpiob_read(self):
        """
        Read GPIO input status

        :returns: received GPIO input status
        :rtype: int32
        :raises SubNotOpenedError:  if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()
        get_par = c_int(1)
        _rc = self._libsub.sub_gpiob_read(self._device, get_par)
        if _rc:
            raise SubDeviceError(self.exc_str())
        return get_par.value

    def sub_gpiob_write(self, set_par, mask):
        """
        Set GPIO output status

        :param set_par: Bits 0-31 of set parameter correspond to GPIO0-GPIO31 output statuses.
        :param mask: Bit in set parameter will take effect only if corresponding mask bit is "1". With mask=0 function will only read current GPIO output status.
        :returns: received GPIO output status.
        :rtype: int32
        :raises SubNotOpenedError: if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()
        get_par = c_int(1)
        _rc = self._libsub.sub_gpiob_write(self._device, set_par, get_par, mask)
        if _rc:
            raise SubDeviceError(self.exc_str())
        return get_par.value

    def sub_rs_set_config(self, config, baud):
        """
        Configure SUB-20 UART.

        :param config: UART configuration
        :param baud: Desired baud rate. Maximum baud rate is 2Mbps.
        :raises SubNotOpenedError:  if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()
        _rc = self._libsub.sub_rs_set_config(self._device, config, baud)
        if _rc:
            raise SubDeviceError(self.exc_str())

    def sub_rs_get_config(self):
        """
        Read current SUB-20 UART configuration.

        :returns: current UART configuration, current UART baud rate
        :rtype: int, int
        :raises SubNotOpenedError:  if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()
        config = c_int(8)
        baud = c_int(8)
        _rc = self._libsub.sub_rs_get_config(self._device, config, baud)
        if _rc:
            raise SubDeviceError(self.exc_str())
        return config.value, baud.value

    def sub_rs_timing(self, flags, tx_space_us, rx_msg_us, rx_byte_us):
        """
        Configure UART transfer timing and order of transmit and receive operations.

        :param flags: handling flags - RS_RX_BEFORE_TX | RS_RX_AFTER_TX | 0
        :param tx_space_us: delay in µs between subsequent byte transmit
        :param rx_msg_us: message reception timeout in µs
        :param rx_byte_us: byte to byte reception timeout in µs
        :raises SubNotOpenedError:  if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()
        _rc = self._libsub.sub_rs_timing(self._device, flags, tx_space_us, rx_msg_us, rx_byte_us)
        if _rc:
            raise SubDeviceError(self.exc_str())

    def sub_rs_xfer(self, tx_buf, tx_sz, rx_buf_sz=MAX_BUF_SZ):
        """
        Transmit and/or receive message(s) via UART

        :param tx_buf: buffer with data to be transmitted
        :param tx_sz: number of bytes to transmit (can be 0 if transmit not required)
        :param rx_buf_sz: maximal number of bytes to receive (can be 0 if reception is not required)
        :returns: number of received bytes
        :rtype: int
        :raises SubNotOpenedError:  if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code
        """
        if not self._device:
            raise SubNotOpenedError()
        _rc = self._libsub.sub_rs_xfer(self._device, tx_buf, tx_sz, self.rx_buf, rx_buf_sz)
        if _rc == -1:
            raise SubDeviceError(self.exc_str())
        return _rc

    def sub_fifo_config(self, config):
        """
        FIFO configuration setup
        :param config: FIFO configuration flags
        :raises SubNotOpenedError:  if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()
        _rc = self._libsub.sub_fifo_config(self._device, config)
        if _rc:
            raise SubDeviceError(self.exc_str())

    def sub_fifo_read(self, to_ms):
        """
        Read 64 bytes from IN FIFO into buffer because this value is highly recommended by documentation
        :param to_ms: read timeout
        :returns: read bytes
        :rtype: int
        :raises SubNotOpenedError:  if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()
        _rc = self._libsub.sub_fifo_read(self._device, self.rx_buf, self.rx_buf_sz, to_ms)
        if _rc < 0:
            raise SubDeviceError(self.exc_str())
        return _rc

    def sub_fifo_write(self, data_buf, sz, to_ms):
        """
        Transfer sz bytes from buffer into OUT FIFO

        :param data_buf: source buffer
        :param sz: buffer size
        :param to_ms: timeout in milliseconds
        :returns: written bytes
        :rtype: int
        :raises SubNotOpenedError:  if the device is not opened
        :raises SubDeviceError: if the wrapped function returned the error code

        """
        if not self._device:
            raise SubNotOpenedError()
        _rc = self._libsub.sub_fifo_write(self._device, data_buf, sz, to_ms)
        if _rc < 0:
            raise SubDeviceError(self.exc_str())
        return _rc

    def exc_str(self):
        return f"{self.strerror(self.sub_errno.value)}[{self.sub_errno.value}]"

    def strerror(self, errno):
        return self._libsub.sub_strerror(errno).decode('UTF-8')

    def close(self):
        if self._device:
            self._libsub.sub_close(self._device)
