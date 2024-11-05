"""(c) Bosch Sensortec GmbH, Reutlingen, Germany.

Open Source as per the BSD-3 Clause

The content of the file is taken from:
COINES_SDK/coines-api/pc/python/coinespy/coines.py

"""

from enum import Enum


class CommandType(Enum):
    DD_SET = 0x01
    DD_GET = 0x02
    DD_STREAMING_SETTINGS = 0x03
    DD_START_STOP_STREAMING_POLLING = 0x06
    DD_START_STOP_STREAMING_INTERRUPT = 0x0A


class CommandId(Enum):
    IO_DIR = 0x04
    IO_VALUE = 0x05
    SPI_MODE = 0x06
    SPI_SPEED = 0x08
    I2C_SPEED = 0x09
    SPI_CHIP_SELECT = 0x0A
    I2C_WRITE_AND_READ = 0x0F
    SPI_WRITE_AND_READ = 0x10
    INTERFACE = 0x11
    SENSOR_SPI_CONFIGURATION = 0x12
    SENSOR_I2C_CONFIGURATION = 0x13
    SHUTTLE_BOARD_VDD_VDDIO_CONFIGURATION = 0x14
    MULTIO_CONFIGURATION = 0x15
    SENSOR_WRITE_AND_READ = 0x16
    BOARD_MODE = 0x18
    SPI_SETTINGS = 0x19
    DELAY = 0x1A
    BOARD_INFORMATION = 0x1F
    SENSOR_WRITE_DELAY_READ = 0x22
    START_STOP_RESPONSE = 0x23
    THIRD_PARTY_WRITE_AND_READ = 0x28
    TIMER_CFG_CMD_ID = 0x29
    UNKNOWN_INSTRUCTION = 0x2B
    APP_SWITCH = 0x30
    SPI_WRITE_AND_READ_16BIT = 0x33
    GENERAL_SETTINGS = 0x43
    START_STOP_POLLING_RESPONSE = 0x46


class CoinesResponse(Enum):
    DD_RESPONSE_SIZE_POSITION = 0x01
    DD_RESPONSE_STATUS_POSITION = 0x03
    DD_RESPONSE_COMMAND_ID_POSITION = 0x04
    DD_RESPONSE_FEATURE_POSITION = 0x05
    DD_RESPONSE_OVERHEAD_BYTES = 0x0D
    DD_RESPONSE_PACKET_LENGTH_MSB_POSITION = 0x08
    DD_RESPONSE_PACKET_LENGTH_LSB_POSITION = 0x09
    DD_RESPONSE_EXTENDED_READ_ID = 0x43


class ErrorCode(Enum):
    SUCCESS = 0
    ERROR_FAILURE = -1
    ERROR_COMM_IO_ERROR = -2
    ERROR_COMM_INIT_FAILED = -3
    ERROR_UNABLE_OPEN_DEVICE = -4
    ERROR_DEVICE_NOT_FOUND = -5
    ERROR_UNABLE_CLAIM_INTERFACE = -6
    ERROR_MEMORY_ALLOCATION = -7
    ERROR_NOT_SUPPORTED = -8
    ERROR_NULL_PTR = -9
    ERROR_COMM_WRONG_RESPONSE = -10
    ERROR_SPI16BIT_NOT_CONFIGURED = -11
    ERROR_SPI_INVALID_BUS_INTERFACE = -12
    ERROR_SPI_CONFIG_EXIST = -13
    ERROR_SPI_BUS_NOT_ENABLED = -14
    ERROR_SPI_CONFIG_FAILED = -15
    ERROR_I2C_INVALID_BUS_INTERFACE = -16
    ERROR_I2C_BUS_NOT_ENABLED = -17
    ERROR_I2C_CONFIG_FAILED = -18
    ERROR_I2C_CONFIG_EXIST = -19
    ERROR_TIMER_INIT_FAILED = -20
    ERROR_TIMER_INVALID_INSTANCE = -21
    ERROR_TIMER_CC_CHANNEL_NOT_AVAILABLE = -22
    ERROR_EEPROM_RESET_FAILED = -23
    ERROR_EEPROM_READ_FAILED = -24
    ERROR_INIT_FAILED = -25
    ERROR_STREAM_NOT_CONFIGURED = -26
    ERROR_STREAM_INVALID_BLOCK_SIZE = -27
    ERROR_STREAM_SENSOR_ALREADY_CONFIGURED = -28
    ERROR_STREAM_CONFIG_MEMORY_FULL = -29
    ERROR_INVALID_PAYLOAD_LEN = -30
    ERROR_CHANNEL_ALLOCATION_FAILED = -31
    ERROR_CHANNEL_DE_ALLOCATION_FAILED = -32
    ERROR_CHANNEL_ASSIGN_FAILED = -33
    ERROR_CHANNEL_ENABLE_FAILED = -34
    ERROR_CHANNEL_DISABLE_FAILED = -35
    ERROR_INVALID_PIN_NUMBER = -36
    ERROR_MAX_SENSOR_COUNT_REACHED = -37
    ERROR_EEPROM_WRITE_FAILED = -38
    ERROR_INVALID_EEPROM_RW_LENGTH = -39
    ERROR_INVALID_SCOM_CONFIG = -40
    ERROR_INVALID_BLE_CONFIG = -41
    ERROR_SCOM_PORT_IN_USE = -42
    ERROR_UART_INIT_FAILED = -43
    ERROR_UART_WRITE_FAILED = -44
    ERROR_UART_INSTANCE_NOT_SUPPORT = -45
    ERROR_BLE_ADAPTOR_NOT_FOUND = -46
    ERROR_ADAPTER_BLUETOOTH_NOT_ENABLED = -47
    ERROR_BLE_PERIPHERAL_NOT_FOUND = -48
    ERROR_BLE_LIBRARY_NOT_LOADED = -49
    ERROR_APP_BOARD_BLE_NOT_FOUND = -50
    ERROR_BLE_COMM_FAILED = -51
    ERROR_INCOMPATIBLE_FIRMWARE = -52
    ERROR_UNDEFINED_CODE = -100


class PinDirection(Enum):
    INPUT = 0
    OUTPUT = 1


class PinValue(Enum):
    LOW = 0
    HIGH = 1


class CommInterface(Enum):
    USB = 0
    SERIAL = 1
    BLE = 2


class StreamingDDMode(Enum):
    BURST_MODE = 1
    NORMAL_MODE = 2
    BURST_MODE_CONTINUOUS = 3


class I2CMode(Enum):
    STANDARD_MODE = 0  # Standard mode - 100kHz
    FAST_MODE = 1  # Fast mode - 400kHz
    SPEED_3_4_MHZ = 2  # High Speed mode - 3.4 MHz
    SPEED_1_7_MHZ = 3  # High Speed mode 2 - 1.7 MHz


class SPISpeed(Enum):
    SPI_10_MHZ = 6
    SPI_7_5_MHZ = 8
    SPI_6_MHZ = 10
    SPI_5_MHZ = 12
    SPI_3_75_MHZ = 16
    SPI_3_MHZ = 20
    SPI_2_5_MHZ = 24
    SPI_2_MHZ = 30
    SPI_1_5_MHZ = 40
    SPI_1_25_MHZ = 48
    SPI_1_2_MHZ = 50
    SPI_1_MHZ = 60
    SPI_750_KHZ = 80
    SPI_600_KHZ = 100
    SPI_500_KHZ = 120
    SPI_400_KHZ = 150
    SPI_300_KHZ = 200
    SPI_250_KHZ = 240


class SPITransferBits(Enum):
    SPI8BIT = 8  # 8 bit register read/write
    SPI16BIT = 16  # 16 bit register read/write


class SPIMode(Enum):
    MODE0 = 0x00  # SPI Mode 0: CPOL=0; CPHA=0
    MODE1 = 0x01  # SPI Mode 1: CPOL=0; CPHA=1
    MODE2 = 0x02  # SPI Mode 2: CPOL=1; CPHA=0
    MODE3 = 0x03  # SPI Mode 3: CPOL=1; CPHA=1


class MultiIOPin(Enum):
    SHUTTLE_PIN_7 = 0x09  # CS pin
    SHUTTLE_PIN_8 = 0x05  # Multi-IO 5
    SHUTTLE_PIN_9 = 0x00  # Multi-IO 0
    SHUTTLE_PIN_14 = 0x01  # Multi-IO 1
    SHUTTLE_PIN_15 = 0x02  # Multi-IO 2
    SHUTTLE_PIN_16 = 0x03  # Multi-IO 3
    SHUTTLE_PIN_19 = 0x08  # Multi-IO 8
    SHUTTLE_PIN_20 = 0x06  # Multi-IO 6
    SHUTTLE_PIN_21 = 0x07  # Multi-IO 7
    SHUTTLE_PIN_22 = 0x04  # Multi-IO 4
    SHUTTLE_PIN_SDO = 0x1F

    # APP3.0 pins
    MINI_SHUTTLE_PIN_1_4 = 0x10  # GPIO0
    MINI_SHUTTLE_PIN_1_5 = 0x11  # GPIO1
    MINI_SHUTTLE_PIN_1_6 = 0x12  # GPIO2/INT1
    MINI_SHUTTLE_PIN_1_7 = 0x13  # GPIO3/INT2
    MINI_SHUTTLE_PIN_2_5 = 0x14  # GPIO4
    MINI_SHUTTLE_PIN_2_6 = 0x15  # GPIO5
    MINI_SHUTTLE_PIN_2_1 = 0x16  # CS
    MINI_SHUTTLE_PIN_2_3 = 0x17  # SDO
    MINI_SHUTTLE_PIN_2_7 = 0x1D  # GPIO6
    MINI_SHUTTLE_PIN_2_8 = 0x1E  # GPIO7


class SensorInterface(Enum):
    SPI = 0
    I2C = 1


class I2CBus(Enum):
    BUS_I2C_0 = 0
    BUS_I2C_1 = 1
    BUS_I2C_MAX = 2


class SPIBus(Enum):
    BUS_SPI_0 = 0
    BUS_SPI_1 = 1
    BUS_SPI_MAX = 2


class StreamingMode(Enum):
    STREAMING_MODE_POLLING = 0
    STREAMING_MODE_INTERRUPT = 1


class StreamingState(Enum):
    STREAMING_START = 1
    STREAMING_STOP = 0


class PinInterruptMode(Enum):
    # Trigger interrupt on pin state change
    PIN_INTERRUPT_CHANGE = 0
    # Trigger interrupt when pin changes from low to high
    PIN_INTERRUPT_RISING_EDGE = 1
    # Trigger interrupt when pin changes from high to low
    PIN_INTERRUPT_FALLING_EDGE = 2
    PIN_INTERRUPT_MODE_MAXIMUM = 4


class TimerConfig(Enum):
    TIMER_STOP = 0
    TIMER_START = 1
    TIMER_RESET = 2


class TimerStampConfig(Enum):
    TIMESTAMP_ENABLE = 0x03
    TIMESTAMP_DISABLE = 0x04


class SamplingUnits(Enum):
    SAMPLING_TIME_IN_MICRO_SEC = 0x01
    SAMPLING_TIME_IN_MILLI_SEC = 0x02


class InterfaceSDO(Enum):
    SDO_LOW = 0
    SDO_HIGH = 1
