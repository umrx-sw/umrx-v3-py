# Examples

These are self-contained examples for using the `umrx-v3-py` with Application Board 3.1.

* [`switch_app_dfu.py`](./switch_app_dfu.py)
* [`switch_app_mtp.py`](./switch_app_mtp.py)

## [`bma400`](https://www.bosch-sensortec.com/products/motion-sensors/accelerometers/bma400/)

The examples in the [`bma400`](./bma400) folder 
show different communication features for the 
[BMA400 shuttle](https://www.bosch-sensortec.com/media/boschsensortec/downloads/shuttle_board_flyer/application_board_3_1/bst-bma400-sf000.pdf)
board:

* [`bma400/bma400_i2c_read_write.py`](./bma400/bma400_i2c_read_write.py) 
* [`bma400/bma400_i2c_polling_streaming.py`](./bma400/bma400_i2c_polling_streaming.py)
* [`bma400/bma400_i2c_interrupt_streaming.py`](./bma400/bma400_i2c_interrupt_streaming.py)
* [`bma400/bma400_spi_read_write.py`](./bma400/bma400_spi_read_write.py)
* [`bma400/bma400_spi_polling_streaming.py`](./bma400/bma400_spi_polling_streaming.py)
* [`bma400/bma400_spi_interrupt_streaming.py`](./bma400/bma400_spi_interrupt_streaming.py)

## [`bma456`](https://www.bosch-sensortec.com/products/motion-sensors/accelerometers/bma456/)

The examples in the [`bma456`](./bma456) folder 
show different communication features for the 
[BMA456 shuttle](https://www.bosch-sensortec.com/media/boschsensortec/downloads/shuttle_board_flyer/application_board_3_1/bst-bma456-sf000.pdf)
board:

* [`bma456/bma456_i2c_read_write.py`](./bma456/bma456_i2c_read_write.py) 
* [`bma456/bma456_i2c_polling_streaming.py`](./bma456/bma456_i2c_polling_streaming.py)
* [`bma456/bma456_i2c_interrupt_streaming.py`](./bma456/bma456_i2c_interrupt_streaming.py)
* [`bma456/bma456_spi_read_write.py`](./bma456/bma456_spi_read_write.py)
* [`bma456/bma456_spi_polling_streaming.py`](./bma456/bma456_spi_polling_streaming.py)
* [`bma456/bma456_spi_interrupt_streaming.py`](./bma456/bma456_spi_interrupt_streaming.py)

## [`bma530`](https://www.bosch-sensortec.com/products/motion-sensors/accelerometers/bma530/)

The examples in the [`bma530`](./bma530) folder 
show different communication features for the 
[BMA530 shuttle](https://www.bosch-sensortec.com/media/boschsensortec/downloads/shuttle_board_flyer/application_board_3_1/bst-bma530-sf000.pdf)
board:

* [`bma530/bma530_i2c_read_write.py`](./bma530/bma530_i2c_read_write.py)
* [`bma530/bma530_i2c_read_write_extended.py`](./bma530/bma530_i2c_read_write_extended.py)
* [`bma530/bma530_i2c_polling_streaming.py`](./bma530/bma530_i2c_polling_streaming.py)
* [`bma530/bma530_i2c_interrupt_streaming.py`](./bma530/bma530_i2c_interrupt_streaming.py)
* [`bma530/bma530_spi_read_write.py`](./bma530/bma530_spi_read_write.py)
* [`bma530/bma530_spi_read_write_extended.py`](./bma530/bma530_spi_read_write_extended.py)
* [`bma530/bma530_spi_polling_streaming.py`](./bma530/bma530_spi_polling_streaming.py)

Note: the SPI interrupt streaming is not available for 
[BMA530 shuttle](https://www.bosch-sensortec.com/media/boschsensortec/downloads/shuttle_board_flyer/application_board_3_1/bst-bma530-sf000.pdf)
because of the sensor pin-out and shuttle schematics (interrupt pins multiplexed with SPI pins).


## [`bma580`](https://www.bosch-sensortec.com/products/motion-sensors/accelerometers/bma580/)

The examples in the [`bma580`](./bma580) folder 
show different communication features for the 
[BMA580 shuttle](https://www.bosch-sensortec.com/media/boschsensortec/downloads/shuttle_board_flyer/application_board_3_1/bst-bma580-sf000.pdf)
board:

* [`bma580/bma580_i2c_read_write.py`](./bma580/bma580_i2c_read_write.py)
* [`bma580/bma580_i2c_read_write_extended.py`](./bma580/bma580_i2c_read_write_extended.py)
* [`bma580/bma580_i2c_polling_streaming.py`](./bma580/bma580_i2c_polling_streaming.py)
* [`bma580/bma580_i2c_interrupt_streaming.py`](./bma580/bma580_i2c_interrupt_streaming.py)
* [`bma580/bma580_spi_read_write.py`](./bma580/bma580_spi_read_write.py)
* [`bma580/bma580_spi_read_write_extended.py`](./bma580/bma580_spi_read_write_extended.py)
* [`bma580/bma580_spi_polling_streaming.py`](./bma580/bma580_spi_polling_streaming.py)

Note: the SPI interrupt streaming is not available for 
[BMA580 shuttle](https://www.bosch-sensortec.com/media/boschsensortec/downloads/shuttle_board_flyer/application_board_3_1/bst-bma580-sf000.pdf)
because of the sensor pin-out and shuttle schematics (interrupt pins multiplexed with SPI pins).


## [`bme280`](https://www.bosch-sensortec.com/products/environmental-sensors/humidity-sensors-bme280/)

The examples in the [`bme280`](./bme280) folder 
show different communication features for the 
[BME280 shuttle](https://www.bosch-sensortec.com/media/boschsensortec/downloads/shuttle_board_flyer/application_board_3_1/bst-bme280-sf000.pdf)
board:

* [`bme280/bme280_i2c_read_write.py`](./bme280/bme280_i2c_read_write.py)
* [`bme280/bme280_i2c_polling_streaming.py`](./bme280/bme280_i2c_polling_streaming.py)
* [`bme280/bme280_spi_read_write.py`](./bme280/bme280_spi_read_write.py)
* [`bme280/bme280_spi_polling_streaming.py`](./bme280/bme280_spi_polling_streaming.py)


## [`bmi088`](https://www.bosch-sensortec.com/products/motion-sensors/imus/bmi088/)

The examples in the [`bmi088`](./bmi088) folder 
show different communication features for the 
[BMI088 shuttle](https://www.bosch-sensortec.com/media/boschsensortec/downloads/shuttle_board_flyer/application_board_3_1/bst-bmi088-sf000.pdf)
board:

* [`bmi088/bmi088_i2c_read_write.py`](./bmi088/bmi088_i2c_read_write.py) 
* [`bmi088/bmi088_i2c_polling_streaming.py`](./bmi088/bmi088_i2c_polling_streaming.py)
* [`bmi088/bmi088_i2c_interrupt_streaming.py`](./bmi088/bmi088_i2c_interrupt_streaming.py)
* [`bmi088/bmi088_spi_read_write.py`](./bmi088/bmi088_spi_read_write.py)
* [`bmi088/bmi088_spi_polling_streaming.py`](./bmi088/bmi088_spi_polling_streaming.py)
* [`bmi088/bmi088_spi_interrupt_streaming.py`](./bmi088/bmi088_spi_interrupt_streaming.py)

## [`bmi323`](https://www.bosch-sensortec.com/products/motion-sensors/imus/bmi323/)

The examples in the [`bmi323`](./bmi323) folder 
show different communication features for the 
[BMI323 shuttle](https://www.bosch-sensortec.com/media/boschsensortec/downloads/shuttle_board_flyer/bst-bmi323-sf000.pdf)
board:

* [`bmi323/bmi323_i2c_read_write.py`](./bmi323/bmi323_i2c_read_write.py) 
* [`bmi323/bmi323_i2c_polling_streaming.py`](./bmi323/bmi323_i2c_polling_streaming.py)
* [`bmi323/bmi323_i2c_interrupt_streaming.py`](./bmi323/bmi323_i2c_interrupt_streaming.py)
* [`bmi323/bmi323_spi_read_write.py`](./bmi323/bmi323_spi_read_write.py)
* [`bmi323/bmi323_spi_polling_streaming.py`](./bmi323/bmi323_spi_polling_streaming.py)
* [`bmi323/bmi323_spi_interrupt_streaming.py`](./bmi323/bmi323_spi_interrupt_streaming.py)

## [`bmp390`](https://www.bosch-sensortec.com/products/environmental-sensors/pressure-sensors/bmp390/)

The examples in the [`bmp390`](./bmp390) folder 
show different communication features for the 
[BMP390 shuttle](https://www.bosch-sensortec.com/media/boschsensortec/downloads/shuttle_board_flyer/application_board_3_1/bst-bmp390-sf000.pdf)
board:

* [`bmp390/bmp390_i2c_read_write.py`](./bmp390/bmp390_i2c_read_write.py) 
* [`bmp390/bmp390_i2c_polling_streaming.py`](./bmp390/bmp390_i2c_polling_streaming.py)
* [`bmp390/bmp390_i2c_interrupt_streaming.py`](./bmp390/bmp390_i2c_interrupt_streaming.py)
* [`bmp390/bmp390_spi_read_write.py`](./bmp390/bmp390_spi_read_write.py)
* [`bmp390/bmp390_spi_polling_streaming.py`](./bmp390/bmp390_spi_polling_streaming.py)
* [`bmp390/bmp390_spi_interrupt_streaming.py`](./bmp390/bmp390_spi_interrupt_streaming.py)



## Need a specific example or do not know how to read data from your sensor?

Let us know, we are happy to help and offer our development expertise.
