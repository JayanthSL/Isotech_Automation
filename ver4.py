from pyModbusTCP.client import ModbusClient
import sys

PLC_IP = '192.168.3.50' 
PLC_PORT = 502         
THERMOCOUPLE_STATUS_REGISTER = 100  
TEMPERATURE_REGISTER = 1          
client = ModbusClient(host=PLC_IP, port=PLC_PORT, auto_open=True)

def check_connection():
    if not client.is_open:
        print("Failed to connect to the PLC. Check the IP address and port.")
        sys.exit(1)

def check_thermocouple_status():
    try:
        status = client.read_holding_registers(THERMOCOUPLE_STATUS_REGISTER, 1)
        if status:
            return status[0] == 1  # Assuming '1' indicates connected, adjust as necessary
        print("Failed to read thermocouple status. Check the register address.")
        return False
    except Exception as e:
        print(f"Error reading thermocouple status: {e}")
        return False

def read_temperature():
    try:
        temperature = client.read_holding_registers(TEMPERATURE_REGISTER, 1)
        if temperature:
            return temperature[0]  # Assuming the temperature value is in the first register
        print("Failed to read temperature. Check the register address.")
        return None
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None

def main():
    check_connection()
    
    if check_thermocouple_status():
        print("Thermocouple is connected.")
        temperature = read_temperature()
        if temperature is not None:
            print(f"Current Temperature: {temperature} °C")
        else:
            print("Failed to read temperature from the PLC.")
    else:
        print("Thermocouple is not connected. Please connect the thermocouple and try again.")

    client.close()

if __name__ == "_main_":
    main()