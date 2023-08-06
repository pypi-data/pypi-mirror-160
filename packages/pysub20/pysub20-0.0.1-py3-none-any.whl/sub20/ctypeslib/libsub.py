from ctypes import POINTER, Structure, c_char_p, c_int, c_double, c_ubyte, c_void_p


class sub_device(Structure):  # pylint: disable=invalid-name
    """
    Dummy for ``sub_device`` structure.
    """
    pass


sub_device_p = POINTER(sub_device)  # pylint: disable=invalid-name


class sub_handle(Structure):  # pylint: disable=invalid-name
    """
    Dummy for ``sub_handle`` structure.
    """
    pass


sub_handle_p = POINTER(sub_handle)  # pylint: disable=invalid-name


class sub_i2c_hs_xfer(Structure):
    """
    Wrapper for ''sub_i2c_hs_xfer'' structure.
    """
    _fields_ = [("sa", c_int),
                ("r_w", c_int),
                ("sa", c_int),
                ("act_sz", c_int),
                ("data", c_char_p),
                ("status", c_int)]


sub_i2c_hs_xfer_p = POINTER(sub_i2c_hs_xfer)


class dll(Structure):
    _fields_ = [("major", c_int),
                ("minor", c_int),
                ("micro", c_int),
                ("nano", c_int)]


class driver(Structure):
    _fields_ = [("major", c_int),
                ("minor", c_int),
                ("micro", c_int),
                ("nano", c_int)]


class sub_device(Structure):
    _fields_ = [("major", c_int),
                ("minor", c_int),
                ("micro", c_int),
                ("nano", c_int)]


class sub_version(Structure):
    _fields_ = [("dll", dll),
                ("driver", driver),
                ("sub_device", sub_device)]


sub_version_p = POINTER(sub_version)

c_int_p = POINTER(c_int)

SIGNATURES = dict(
    sub_find_devices=([sub_device_p], sub_device_p),
    sub_open=([sub_device_p], sub_handle_p),
    sub_get_serial_number=([sub_handle_p, c_char_p], c_int),
    sub_get_product_id=([sub_handle_p, c_char_p], c_int),
    sub_get_version=([sub_handle_p], c_void_p),
    sub_reset=([sub_handle_p], c_int),

    sub_eep_read=([sub_handle_p, c_int, c_char_p, c_int], c_int),
    sub_eep_write=([sub_handle_p, c_int, c_char_p, c_int], c_int),

    sub_i2c_freq=([sub_handle_p, c_int_p], c_int),
    sub_i2c_config=([sub_handle_p, c_int, c_int], c_int),
    sub_i2c_start=([sub_handle_p], c_int),
    sub_i2c_stop=([sub_handle_p], c_int),
    sub_i2c_scan=([sub_handle_p, c_int_p, c_char_p], c_int),
    sub_i2c_read=([sub_handle_p, c_int, c_int, c_int, c_char_p, c_int], c_int),
    sub_i2c_write=([sub_handle_p, c_int, c_int, c_int, c_char_p, c_int], c_int),
    sub_i2c_transfer=([sub_handle_p, c_int, c_char_p, c_int, c_char_p, c_int], c_int),
    sub_i2c_hs_rw=([sub_handle_p, c_int, c_int, sub_i2c_hs_xfer_p], c_int),

    sub_bb_i2c_config=([sub_handle_p, c_int, c_int], c_int),
    sub_bb_i2c_scan=([sub_handle_p, c_int, c_int_p, c_char_p], c_int),
    sub_bb_i2c_read=([sub_handle_p, c_int, c_int, c_int, c_int, c_char_p, c_int], c_int),
    sub_bb_i2c_write=([sub_handle_p, c_int, c_int, c_int, c_int, c_char_p, c_int], c_int),

    sub_spi_config=([sub_handle_p, c_int, c_int_p], c_int),
    sub_spi_transfer=([sub_handle_p, c_char_p, c_char_p, c_int, c_int], c_int),
    sub_spi_transfer_ess=([sub_handle_p, c_char_p, c_char_p, c_int, c_char_p], c_int),
    sub_sdio_transfer=([sub_handle_p, c_char_p, c_char_p, c_int, c_int, c_int], c_int),

    sub_gpio_config=([sub_handle_p, c_int, c_int_p, c_int], c_int),
    sub_gpio_read=([sub_handle_p, c_int_p], c_int),
    sub_gpio_write=([sub_handle_p, c_int, c_int_p, c_int], c_int),
    sub_gpiob_config=([sub_handle_p, c_int, c_int_p, c_int], c_int),
    sub_gpiob_read=([sub_handle_p, c_int_p], c_int),
    sub_gpiob_write=([sub_handle_p, c_int, c_int_p, c_int], c_int),

    sub_gpio_wdt_set=([sub_handle_p, c_int, c_int, c_int], c_int),
    sub_gpio_wdt_get=([sub_handle_p, c_int_p, c_int_p, c_int_p, POINTER(c_ubyte)], c_int),

    sub_edge_config=([sub_handle_p, c_int, c_int_p], c_int),
    sub_edge_read=([sub_handle_p, c_int_p, c_int_p], c_int),

    sub_fpwm_config=([sub_handle_p, c_double, c_int], c_int),
    sub_fpwm_set=([sub_handle_p, c_int, c_double], c_int),

    sub_adc_config=([sub_handle_p, c_int], c_int),
    sub_adc_read=([sub_handle_p, c_int_p, c_int_p, c_int], c_int),
    sub_adc_single=([sub_handle_p, c_int_p, c_int], c_int),

    sub_lcd_write=([sub_handle_p, c_char_p], c_int),

    sub_rs_set_config=([sub_handle_p, c_int, c_int], c_int),
    sub_rs_get_config=([sub_handle_p, c_int_p, c_int_p], c_int),
    sub_rs_timing=([sub_handle_p, c_int, c_int, c_int, c_int], c_int),
    sub_rs_xfer=([sub_handle_p, c_char_p, c_int, c_char_p, c_int], c_int),

    sub_fifo_config=([sub_handle_p, c_int], c_int),
    sub_fifo_read=([sub_handle_p, c_char_p, c_int, c_int], c_int),

    sub_strerror=([c_int], c_char_p),
    sub_close=([sub_handle_p], None),

)
