from logger_setup import logger_config

logger = logger_config()

class ChamberControl:
    def __init__(self, modbus_client, start_register, stop_register):
        """
        Initializes the ChamberControl class.
        
        Arguments:
        - client: Modbus client instance for communication with the PLC.
        - start_register: Modbus register for starting the chamber.
        - stop_register: Modbus register for stopping the chamber.
        """
        self.client = modbus_client
        self.start_register = start_register
        self.stop_register = stop_register
        # self.logger = logging.getLogger(__name__)

    def start_chamber(self):
        """
        Sends a command to start the chamber.
        """
        logger.info(f"Attempting to start the chamber...")
        try:
            self.client.write_register(self.start_register, 1)
            logger.info(f"Chamber started successfully.")
        except Exception as e:
            logger.error(f"Failed to start the chamber.")
            logger.exception(e)

    def stop_chamber(self):
        """
        Sends a command to stop the chamber.
        """
        logger.info("Attempting to stop the chamber...")
        try:
            self.client.write_register(self.stop_register, 0)
            logger.info(f"Chamber stopped successfully.")
        except Exception as e:
            logger.error(f"Failed to stop the chamber.")
            logger.exception(e)
