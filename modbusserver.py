from pyModbusTCP.client import ModbusClient

class ModbusServerHandler:
    """
    Handles Modbus communication with a PLC server.
    """
    def __init__(self, ip, port):
        """
        Initializes the Modbus client with the given IP and port.

        Args:
            ip (str): The IP address of the PLC server.
            port (int): The port number for the Modbus server.
        """
        self.client = ModbusClient(host=ip, port=port, auto_open=True)
    
    def read_register(self, register_address):
        """
        Reads a value from the specified Modbus register.

        Args:
            register_address (int): The address of the register to read.
        """
        return self.client.read_holding_registers(register_address, 1)
    
    def write_register(self, register_address, value):
        """
        Writes a value to the specified Modbus register.

        Args:
            register_address (int): The address of the register to write to.
            value (int): The value to write.
        """
        self.client.write_single_register(register_address, value)
    
    def close_connection(self):
        """
        Closes the connection to the Modbus server.
        """
        self.client.close()
