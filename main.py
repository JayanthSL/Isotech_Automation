import time
import logging
from pyModbusTCP.client import ModbusClient
from config import (PLC_IP, PLC_PORT, PARAMETER_MODBUS_ADDRESSES, SEG_MODBUS_ADDRESSES,
                    MIN_TEMPERATURE, MAX_TEMPERATURE, MIN_HUMIDITY, MAX_HUMIDITY,
                    MAX_TEMP_RAMP_RATE, MAX_HUMIDITY_RAMP_RATE)

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('isotech.logs')
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Connect to Siemens PLC
client = ModbusClient(host=PLC_IP, port=PLC_PORT, auto_open=True)

temperature_register = PARAMETER_MODBUS_ADDRESSES['Programmer.Run.PSP']
humidity_register = SEG_MODBUS_ADDRESSES['SEG_PTD_1[1]']

if not client.is_open:
    logger.error("Failed to connect to the PLC. Please check the connection.")
    exit()

logger.info("Reading current temperature and humidity from the PLC.")
temperature = client.read_holding_registers(temperature_register, 1)
humidity = client.read_holding_registers(humidity_register, 1)

if temperature and humidity:
    current_temperature = temperature[0]
    current_humidity = humidity[0]
    logger.info(f"Current Temperature: {current_temperature}")
    logger.info(f"Current Humidity: {current_humidity}")

    try:
        new_temperature = int(input(f"Enter new temperature setpoint ({MIN_TEMPERATURE} to {MAX_TEMPERATURE}): "))
        new_humidity = int(input(f"Enter new humidity setpoint ({MIN_HUMIDITY} to {MAX_HUMIDITY}): "))

        if not (MIN_TEMPERATURE <= new_temperature <= MAX_TEMPERATURE):
            logger.error(f"Temperature setpoint must be between {MIN_TEMPERATURE} and {MAX_TEMPERATURE}.")
            exit()

        if not (MIN_HUMIDITY <= new_humidity <= MAX_HUMIDITY):
            logger.error(f"Humidity setpoint must be between {MIN_HUMIDITY} and {MAX_HUMIDITY}.")
            exit()

        temp_ramp_rate = float(input(f"Enter temperature ramp rate (degrees per minute, max {MAX_TEMP_RAMP_RATE}): "))
        humidity_ramp_rate = float(input(f"Enter humidity ramp rate (percent per minute, max {MAX_HUMIDITY_RAMP_RATE}): "))

        if temp_ramp_rate > MAX_TEMP_RAMP_RATE or temp_ramp_rate <= 0:
            logger.error(f"Invalid temperature ramp rate. Must be > 0 and ≤ {MAX_TEMP_RAMP_RATE}.")
            exit()

        if humidity_ramp_rate > MAX_HUMIDITY_RAMP_RATE or humidity_ramp_rate <= 0:
            logger.error(f"Invalid humidity ramp rate. Must be > 0 and ≤ {MAX_HUMIDITY_RAMP_RATE}.")
            exit()

        # Adjust temperature
        if current_temperature != new_temperature:
            logger.info(f"Adjusting temperature from {current_temperature} to {new_temperature}...")
            while current_temperature != new_temperature:
                step = temp_ramp_rate if current_temperature < new_temperature else -temp_ramp_rate
                current_temperature += step
                current_temperature = max(min(new_temperature, current_temperature), min(current_temperature, new_temperature))
                client.write_single_register(temperature_register, int(current_temperature))
                logger.info(f"Current Temperature: {current_temperature:.2f}")
                time.sleep(60)

        # Adjust humidity
        if current_humidity != new_humidity:
            logger.info(f"Adjusting humidity from {current_humidity} to {new_humidity}...")
            while current_humidity != new_humidity:
                step = humidity_ramp_rate if current_humidity < new_humidity else -humidity_ramp_rate
                current_humidity += step
                current_humidity = max(min(new_humidity, current_humidity), min(current_humidity, new_humidity))
                client.write_single_register(humidity_register, int(current_humidity))
                logger.info(f"Current Humidity: {current_humidity:.2f}")
                time.sleep(60)

        logger.info(f"Successfully updated temperature to {new_temperature} and humidity to {new_humidity}.")

    except ValueError as e:
        logger.error("Invalid input. Please enter valid integers or floats for temperature, humidity, and ramp rates.")
        logger.exception(e)
else:
    logger.error("Failed to read temperature or humidity from the PLC.")

logger.info("Closing the connection to the PLC.")
client.close()
