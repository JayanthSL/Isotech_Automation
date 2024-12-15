from modbusserver import ModbusServerHandler
from temperature_humidity_controller import TemperatureHumidityController
from loggerconfig import logger_config
from config import (PLC_IP, PLC_PORT, PARAMETER_MODBUS_ADDRESSES, SEG_MODBUS_ADDRESSES,
                    MIN_TEMPERATURE, MAX_TEMPERATURE, MIN_HUMIDITY, MAX_HUMIDITY,
                    MAX_TEMP_RAMP_RATE, MAX_HUMIDITY_RAMP_RATE)

# Configure logger
logger = logger_config()

# Connect to Siemens PLC
modbus_client = ModbusServerHandler(PLC_IP, PLC_PORT)

# Create controller for temperature and humidity
controller = TemperatureHumidityController(modbus_client, 
                                           PARAMETER_MODBUS_ADDRESSES['Programmer.Run.PSP'], 
                                           SEG_MODBUS_ADDRESSES['SEG_PTD_1[1]'])

if not modbus_client.client.is_open:
    logger.error("Failed to connect to the PLC. Please check the connection.")
    exit()

logger.info("Reading current temperature and humidity from the PLC.")
temperature = modbus_client.read_register(PARAMETER_MODBUS_ADDRESSES['Programmer.Run.PSP'])
humidity = modbus_client.read_register(SEG_MODBUS_ADDRESSES['SEG_PTD_1[1]'])

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

        # Adjust temperature and humidity
        current_temperature = controller.adjust_temperature(current_temperature, new_temperature, temp_ramp_rate)
        current_humidity = controller.adjust_humidity(current_humidity, new_humidity, humidity_ramp_rate)

        logger.info(f"Successfully updated temperature to {new_temperature} and humidity to {new_humidity}.")

    except ValueError as e:
        logger.error("Invalid input. Please enter valid integers or floats for temperature, humidity, and ramp rates.")
        logger.exception(e)
else:
    logger.error("Failed to read temperature or humidity from the PLC.")

logger.info("Closing the connection to the PLC.")
modbus_client.close_connection()
