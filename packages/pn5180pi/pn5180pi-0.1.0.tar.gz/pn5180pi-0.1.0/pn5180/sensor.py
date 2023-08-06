from abc import ABC, abstractmethod
import RPi.GPIO as GPIO
import spidev
from time import sleep
from typing import Optional

from pn5180.definitions import *


class Sensor(ABC):
    """
    Abstract class from which all other sensor protocol classes are subclassed
    """

    def __init__(
        self,
        spi_bus: int = 0,
        spi_device: int = 0,
        busy_pin: int = 25,
        reset_pin: int = 7,
        max_speed: int = 115200,
        verbose: bool = False,
    ) -> None:
        self._verbose: bool = verbose
        self._spi = spidev.SpiDev(spi_bus, spi_device)
        self._spi.max_speed_hz = max_speed
        self._busy_pin = busy_pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(busy_pin, GPIO.IN)
        self._reset_pin = reset_pin
        GPIO.setup(reset_pin, GPIO.OUT)
        GPIO.output(reset_pin, GPIO.LOW)
        sleep(1)
        GPIO.output(reset_pin, GPIO.HIGH)
        sleep(1)

    def _wait_ready(self) -> None:
        """Waits for busy pin to be low"""
        # self._log("Checking if chip is ready")
        if GPIO.input(self._busy_pin):
            # self._log("Chip is not ready; waiting...")
            GPIO.wait_for_edge(self._busy_pin, GPIO.FALLING, timeout=10)
        # self._log("Chip is ready; continuing")

    def _log(self, message: str) -> None:
        if self._verbose:
            print(message)

    def _read(self, length: int) -> list:
        self._log(f"Reading {length} bytes")
        return self._spi.readbytes(length)

    def _write(self, bytes: list) -> None:
        self._wait_ready()
        self._spi.writebytes(bytes)
        self._log(f"Sent frame: {bytes}")
        self._wait_ready()

    def _turn_on_rf_field(self, parameter: int = 0x00) -> None:
        self._write([CMD_RF_ON, parameter])

    def _turn_off_rf_field(self) -> None:
        # second parameter is a dummy byte
        self._write([CMD_RF_OFF, 0x00])

    def _clear_interrupt_register(self) -> None:
        # write all 1s into the bits actually used
        self._write([CMD_WRITE_REGISTER, REG_IRQ_CLEAR, 0xFF, 0xFF, 0xFF, 0xFF])

    def _read_data_cmd(self) -> None:
        self._write([CMD_READ_DATA, 0x00])

    def _read_irq(self) -> None:
        self._write([CMD_READ_REGISTER, REG_IRQ_CLEAR])

    @abstractmethod
    def read_tag(self) -> Optional[str]:
        pass


class ISO15693Sensor(Sensor):
    """
    Driver to easily read/write ISO15693 tags with the PN5180
    """

    def _load_protocol(self) -> None:
        self._write([CMD_LOAD_RF_CONFIGURATION, TX_ISO_15693_ASK10_26, RX_ISO_15693_26])

    def _set_idle_state(self) -> None:
        # clear idle bits, keep all other bits the same
        self._write(
            [CMD_WRITE_REGISTER_AND_MASK, REG_SYSTEM_CONFIG, 0xF8, 0xFF, 0xFF, 0xFF]
        )

    def _activate_transceive_routine(self) -> None:
        # set transceive bits, keep all other bits the same
        self._write(
            [CMD_WRITE_REGISTER_OR_MASK, REG_SYSTEM_CONFIG, 0x03, 0x00, 0x00, 0x00]
        )

    def _activate_inventory_mode(self) -> None:
        self._write([CMD_SEND_DATA, 0x00, 0x26, 0x01, 0x00])

    def _set_send_eof(self) -> None:
        # clear bits 7, 8, and 11, keep all other bits the same
        self._write(
            [CMD_WRITE_REGISTER_AND_MASK, REG_TX_CONFIG, 0x3F, 0xFB, 0xFF, 0xFF]
        )

    def _send_eof(self) -> None:
        self._write([CMD_SEND_DATA, 0x00])

    def _get_card_response_bytes(self) -> int:
        self._write([CMD_READ_REGISTER, REG_RX_STATUS])
        response = self._read(REGISTER_SIZE)
        self._log(f"Received {response}")
        return response[0]

    def read_tag(self) -> Optional[str]:
        response = None
        self._load_protocol()
        self._turn_on_rf_field()
        self._clear_interrupt_register()
        self._set_idle_state()
        self._activate_transceive_routine()
        self._activate_inventory_mode()
        sleep(0.02)
        response_bytes = self._get_card_response_bytes()
        if response_bytes:
            self._read_data_cmd()
            buffer_response = self._read(response_bytes)
            self._log(f"Received: {buffer_response}")
            response = "".join([f"{byte:02x}:" for byte in buffer_response])[:-1]
        self._set_send_eof()
        self._set_idle_state()
        self._activate_transceive_routine()
        self._clear_interrupt_register()
        self._send_eof()
        self._turn_off_rf_field()

        return response
