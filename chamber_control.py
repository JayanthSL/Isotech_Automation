from logger_setup import logger_config
from modbus_client import ModbusServerHandler
from config import (PLC_IP, PLC_PORT, START_CHAMBER, STOP_CHAMBER)

modbus_client = ModbusServerHandler(PLC_IP, PLC_PORT)

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
        start = modbus_client.read_register(START_CHAMBER)
        if start:
            start2 = start[0]
            logger.info({start2})
            while True:
                try:
                    modbus_client.write_register(START_CHAMBER, 1)
                    logger.info(f"Chamber started successfully.")
                except Exception as e:
                    logger.error(f"Failed to start the chamber.")
                    logger.exception(e)
        else:
            logger.error("Error")
        # try:
        #     # modbus_client.read_register(START_CHAMBER)

        #     logger.info(f"Chamber started successfully.")
        # except Exception as e:
        #     logger.error(f"Failed to start the chamber.")
        #     logger.exception(e)

    def stop_chamber(self):
        """
        Sends a command to stop the chamber.
        """
        logger.info("Attempting to stop the chamber...")
        start3 = modbus_client.read_register(STOP_CHAMBER)
        if start3:
            start4 = start3[0]
            logger.info({start4})    
            while True:    
                try:
                    self.client.write_register(self.stop_register, 0)
                    logger.info(f"Chamber stopped successfully.")
                except Exception as e:
                    logger.error(f"Failed to stop the chamber.")
                    logger.exception(e)
        else:
            logger.error(f"Error")