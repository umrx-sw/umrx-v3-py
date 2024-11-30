# Python communication with COINES firmware

[![Static analysis and Unit tests](https://github.com/umrx-sw/umrx-v3-py/actions/workflows/python-lint-and-test.yml/badge.svg)](https://github.com/umrx-sw/umrx-v3-py/actions/workflows/python-lint-and-test.yml)

`python3` communication with COINES firmware on 
[Application Board 3.1](https://www.bosch-sensortec.com/software-tools/tools/application-board-3-1/) or 
[3.0](https://www.bosch-sensortec.com/software-tools/tools/application-board-3-0/) hardware.

Install the latest version from [pypi](https://pypi.org/project/umrx-app-v3/):
```bash
pip install umrx-app-v3
```

The `umrx-app-v3` project implements in `python3` COINES communication protocol 
to interact with the micro-controller (MCU) and read the sensor data from the 
[Application Board 3.1](https://www.bosch-sensortec.com/software-tools/tools/application-board-3-1/) and 
[3.0](https://www.bosch-sensortec.com/software-tools/tools/application-board-3-0/) when 
board is programmed with BST default firmware.

Unlike python bindings from [COINES SDK](https://github.com/boschsensortec/COINES_SDK)
which load pre-compiled OS-dependent C library,
this project is built entirely in python and requires only 
[`pyserial`](https://pypi.org/project/pyserial/)
and 
[`pyusb`](https://pypi.org/project/pyusb/) dependencies.

## Features

* Support [Application Board 3.1](https://www.bosch-sensortec.com/software-tools/tools/application-board-3-1/) 
  and 
  [Application Board 3.0](https://www.bosch-sensortec.com/software-tools/tools/application-board-3-0/);
* Configure shuttle pins, set pin levels;
* Switch ON/OFF `VDD` and `VDDIO` of the shuttle board to power the sensor;
* Read / write the sensor registers using the I2C protocol;
* Read / write the sensor registers using the SPI protocol;
* Configure and receive streaming packets:
    * **Polling** streaming: sensor registers are read in bulk at regular intervals;
    * **Interrupt** streaming: sensor registers are read in bulk when sensor reports data ready over interrupt pin;
* Switch application to 
  [DFU](https://www.usb.org/document-library/device-firmware-upgrade-11-new-version-31-aug-2004) or 
  [MTP](https://en.wikipedia.org/wiki/Media_Transfer_Protocol);
* Enable MCU time stamp (works only with Application Board 3.0).


## Installation 

Communication with firmware happens either via USB (for Application Board 3.0) 
or serial port over USB (for Application Board 3.1).
Reading / writing USB (or serial) devices is often a privileged operation. 
Below we describe OS-specific setup steps to be able to use the package. 

### OS prerequisites

#### Linux

To access USB device on Linux as a regular user, one needs to install the `udev`-rules.
Create the file `/etc/udev/rules.d/application_board.rules` with the following content:

```bash
# Application Board 3.0
SUBSYSTEM=="usb", ATTRS{idVendor}=="152a", ATTRS{idProduct}=="80c0", ACTION=="add", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
SUBSYSTEM=="usb", ATTRS{idVendor}=="108c", ATTRS{idProduct}=="ab3d", ACTION=="add", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
SUBSYSTEM=="usb", ATTRS{idVendor}=="108c", ATTRS{idProduct}=="ab3f", ACTION=="add", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"

# Application Board 3.1
SUBSYSTEM=="usb", ATTRS{idVendor}=="108c", ATTRS{idProduct}=="ab38", ACTION=="add", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
SUBSYSTEM=="usb", ATTRS{idVendor}=="108c", ATTRS{idProduct}=="ab39", ACTION=="add", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
SUBSYSTEM=="usb", ATTRS{idVendor}=="108c", ATTRS{idProduct}=="ab3a", ACTION=="add", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
```

The file can be created with the following command:
```bash
sudo bash -c 'cat <<EOF >>/etc/udev/rules.d/application_board.rules
# Application Board 3.0
SUBSYSTEM=="usb", ATTRS{idVendor}=="152a", ATTRS{idProduct}=="80c0", ACTION=="add", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
SUBSYSTEM=="usb", ATTRS{idVendor}=="108c", ATTRS{idProduct}=="ab3d", ACTION=="add", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
SUBSYSTEM=="usb", ATTRS{idVendor}=="108c", ATTRS{idProduct}=="ab3f", ACTION=="add", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"

# Application Board 3.1
SUBSYSTEM=="usb", ATTRS{idVendor}=="108c", ATTRS{idProduct}=="ab38", ACTION=="add", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
SUBSYSTEM=="usb", ATTRS{idVendor}=="108c", ATTRS{idProduct}=="ab39", ACTION=="add", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
SUBSYSTEM=="usb", ATTRS{idVendor}=="108c", ATTRS{idProduct}=="ab3a", ACTION=="add", MODE="0666", ENV{ID_MM_DEVICE_IGNORE}="1"
EOF'
```

Reload the udev-rules:

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

To access serial devices on Linux as a regular user, one needs to be a member of the `dialout` group.

```bash
sudo usermod -a -G dialout <your-user-name>
```

#### Windows

Install [libusb-1](https://github.com/libusb/libusb) via `vcpkg` by following 
these [instructions](https://github.com/libusb/libusb/wiki/Windows#user-content-vcpkg_port).

Add the path where the `*.DLL` libraries are located to the `PATH` environment variable.

Use [`zadig`](https://zadig.akeo.ie/) to install the drivers for the boards:

* For Application Board 3.1 install CDC serial driver:

* For Application Board 3.0 install WinUSB:



#### Mac OS

Install [Homebrew](https://brew.sh/).

Install [libusb](https://formulae.brew.sh/formula/libusb):
```bash
brew install libusb
```


Execute the python scripts with `sudo` to read/write USB device.

### Install using pip

```bash
pip install umrx-app-v3
```


### Install from source

To install the package from source:
1. clone the repository, and 
2. run in the repo root:
```bash
pip install poetry
poetry install 
poetry shell
```

## Supported python version

The project was developed with `python-3.12` although it might work earlier python versions `>=3.9`.

## Quick start

The examples below are self-contained and can be copy-pasted as is.

### Terminology

Bosch offers two hardware revisions:
* [Application Board 3.1](https://www.bosch-sensortec.com/software-tools/tools/application-board-3-1/), **3.1** HW
* [Application Board 3.0](https://www.bosch-sensortec.com/software-tools/tools/application-board-3-0/), **3.0** HW

Although both boards use [`nRF52840`](https://www.nordicsemi.com/Products/nRF52840)
(and are based on [`NINA-B30*`](https://www.u-blox.com/en/product/nina-b30-series-open-cpu-0) modules),
they differ in hardware and firmware.

In `umrx-v3-py` code to differentiate the boards we use 
`v3_rev1` (for _v3, revision 1_) suffix for **3.1** HW
and 
`v3_rev0` (for _v3, revision 0_) suffix for **3.0** HW.

### Create the board object

Create the board object and initialize (connect to board and open communication):

```python
from umrx_app_v3.mcu_board.app_board_v3_rev1 import ApplicationBoardV3Rev1

board = ApplicationBoardV3Rev1()
# initialize board communication 
board.initialize()
```

### Configure shuttle pins

```python
from umrx_app_v3.mcu_board.app_board_v3_rev1 import ApplicationBoardV3Rev1
from umrx_app_v3.mcu_board.bst_protocol_constants import MultiIOPin, PinDirection, PinValue

board = ApplicationBoardV3Rev1()
board.initialize()
# configure shuttle pin P2.6 as output and set to high 
board.set_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_6, PinDirection.OUTPUT, PinValue.HIGH)
```

### Supply power to shuttle

```python
from umrx_app_v3.mcu_board.app_board_v3_rev1 import ApplicationBoardV3Rev1

board = ApplicationBoardV3Rev1()
board.initialize()
# set VDD to 3.3 V, VDDIO to 3.3 V
board.set_vdd_vddio(3.3, 3.3)
```

### Configure communication interface

#### I2C

```python
import time
from umrx_app_v3.mcu_board.app_board_v3_rev1 import ApplicationBoardV3Rev1
from umrx_app_v3.mcu_board.bst_protocol_constants import MultiIOPin, PinDirection, PinValue

board = ApplicationBoardV3Rev1()
board.initialize()
board.set_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_6, PinDirection.OUTPUT, PinValue.HIGH)
board.set_vdd_vddio(3.3, 3.3)
time.sleep(0.01)
board.configure_i2c()
```

#### SPI

```python
import time
from umrx_app_v3.mcu_board.app_board_v3_rev1 import ApplicationBoardV3Rev1
from umrx_app_v3.mcu_board.bst_protocol_constants import MultiIOPin, PinDirection, PinValue, SPIBus
from umrx_app_v3.mcu_board.commands.spi import SPIConfigureCmd

board = ApplicationBoardV3Rev1()
board.initialize()
board.set_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_1, PinDirection.OUTPUT, PinValue.HIGH)
board.set_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_5, PinDirection.OUTPUT, PinValue.HIGH)
board.set_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_6, PinDirection.OUTPUT, PinValue.LOW)
board.set_vdd_vddio(3.3, 3.3)
time.sleep(0.01)
SPIConfigureCmd.set_bus(SPIBus.BUS_1)
board.configure_spi()
```

### Read / write registers

#### I2C
```python
import time
from umrx_app_v3.mcu_board.app_board_v3_rev1 import ApplicationBoardV3Rev1
from umrx_app_v3.mcu_board.bst_protocol_constants import MultiIOPin, PinDirection, PinValue

board = ApplicationBoardV3Rev1()
board.initialize()
board.start_communication()
board.set_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_6, PinDirection.OUTPUT, PinValue.HIGH)
board.set_vdd_vddio(3.3, 3.3)
time.sleep(0.1)
board.configure_i2c()
result = board.read_i2c(i2c_address=0x68, register_address=0x0, bytes_to_read=1)
print(result)
```
#### SPI

```python
import time
from umrx_app_v3.mcu_board.app_board_v3_rev1 import ApplicationBoardV3Rev1
from umrx_app_v3.mcu_board.bst_protocol_constants import MultiIOPin, PinDirection, PinValue, SPIBus
from umrx_app_v3.mcu_board.commands.spi import SPIConfigureCmd

board = ApplicationBoardV3Rev1()
board.initialize()
board.set_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_1, PinDirection.OUTPUT, PinValue.HIGH)
board.set_pin_config(MultiIOPin.MINI_SHUTTLE_PIN_2_6, PinDirection.OUTPUT, PinValue.LOW)
board.set_vdd_vddio(3.3, 3.3)
time.sleep(0.01)
SPIConfigureCmd.set_bus(SPIBus.BUS_1)
board.configure_spi()
result = board.read_spi(cs_pin=MultiIOPin.MINI_SHUTTLE_PIN_2_5, register_address=0x0, bytes_to_read=1)
print(result)
```

### Examples

Take a look at the additional [examples](./examples).

## Default firmware

The code was developed and tested with the _default_ firmware the **3.0** and **3.1** boards
were pre-programmed with.

If you want to program you board with the same firmware, follow instructions from this 
[repo](https://github.com/umrx-sw/bst-default-firmware).
