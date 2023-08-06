import abc


class SubDeviceError(Exception):
    __metaclass__ = abc.ABCMeta


class SubNotFoundError(SubDeviceError):
    __metaclass__ = abc.ABCMeta


class I2CDevicesNotFoundError(SubDeviceError):
    __metaclass__ = abc.ABCMeta


class SubNotOpenedError(SubDeviceError):
    __metaclass__ = abc.ABCMeta