from logger_setup import logger_config
from modbus_client import ModbusServerHandler
from config import (PLC_IP, PLC_PORT, START_CHAMBER, STOP_CHAMBER)
import time

modbus_client = ModbusServerHandler(PLC_IP, PLC_PORT)

logger = logger_config()

class ChamberControl:
    def __init__(self, modbus_client, start_register, stop_register):
        """
        Initializes the ChamberControl class.
        
        Arguments:
        - modbus_client: Modbus client instance for communication with the PLC.
        - start_register: Modbus register for starting the chamber.
        - stop_register: Modbus register for stopping the chamber.
        """
        self.client = modbus_client
        self.start_register = start_register
        self.stop_register = stop_register

    def start_chamber(self):
        """
        Sends a command to start the chamber.
        """
        logger.info("Attempting to start the chamber...")
        start = self.client.read_register(self.start_register)
        if start:
            logger.info(f"Current value in start register: {start[0]}")
            try:
                self.client.write_register(self.start_register, 1)
                logger.info("Chamber started successfully.")
            except Exception as e:
                logger.error("Failed to start the chamber.")
                logger.exception(e)
        else:
            logger.error("Failed to read the start register.")

    def stop_chamber(self):
        """
        Sends a command to stop the chamber.
        """
        logger.info("Attempting to stop the chamber...")
        stop = self.client.read_register(self.stop_register)
        if stop:
            logger.info(f"Current value in stop register: {stop[0]}")
            try:
                self.client.write_register(self.stop_register, 0)
                logger.info("Chamber stopped successfully.")
            except Exception as e:
                logger.error("Failed to stop the chamber.")
                logger.exception(e)
        else:
            logger.error("Failed to read the stop register.")


if __name__ == "__main__":
    chamber_control = ChamberControl(modbus_client, START_CHAMBER, STOP_CHAMBER)

    while True:
        print("\nChamber Control Menu:")
        print("1. Start Chamber")
        print("2. Stop Chamber")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            chamber_control.start_chamber()
        elif choice == "2":
            chamber_control.stop_chamber()
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
