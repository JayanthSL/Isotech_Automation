from pyModbusTCP.client import ModbusClient

class ModbusServerHandler:
    def __init__(self, ip, port):
        self.client = ModbusClient(host=ip, port=port, auto_open=True)
    
    def read_register(self, register_address):
        return self.client.read_holding_registers(register_address, 1)
    
    def write_register(self, register_address, value):
        self.client.write_single_register(register_address, value)
    
    def close_connection(self):
        self.client.close()
