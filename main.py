import time
import logging
from pyModbusTCP.client import ModbusClient

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create file handler to save logs to a file
file_handler = logging.FileHandler('isotech.logs')
file_handler.setLevel(logging.DEBUG)  # Capture all log levels

# Create console handler to also display logs on the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Display only info and above on the console

# Create formatter and add it to both handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Connect to Siemens PLC (replace 'PLC_IP' with your actual PLC IP address)
client = ModbusClient(host='192.168.3.50', port=502, auto_open=True)

# Define register addresses based on the extracted mappings
parameter_modbus_addresses = {
    'Programmer.Run.Mode': 23,
    'Programmer.Run.PSP': 1,  # This is the temperature register
    'Programmer.Run.SegmentNumber': 56,
    'Programmer.Run.SegmentType': 29,
    'Programmer.Run.SegmentTimeLeft': 63
}

seg_modbus_addresses = {
    'SEG_PTD_1[0]': 1,  # This is the humidity register
    'SEG_PTD_1[1]': 2,
    'SEG_PTD_1[2]': 3
}

# Set the temperature and humidity registers based on the mappings
temperature_register = parameter_modbus_addresses['Programmer.Run.PSP']  # Register for temperature
humidity_register = seg_modbus_addresses['SEG_PTD_1[1]']  # Register for humidity

# Max ramp rates
MAX_TEMP_RAMP_RATE = 1  # Max ramp rate for temperature (1 degree per minute)
MAX_HUMIDITY_RAMP_RATE = 1  # Max ramp rate for humidity (1 percent per minute)

# Step 1: Read the current temperature and humidity from the PLC
logger.info("Reading current temperature and humidity from the PLC.")
temperature = client.read_holding_registers(1, 1)
humidity = client.read_holding_registers(2, 1)

if temperature and humidity:
    current_temperature = temperature[0]
    current_humidity = humidity[0]
    logger.info(f"Current Temperature: {current_temperature}")
    logger.info(f"Current Humidity: {current_humidity}")

    # Step 2: Prompt user for new temperature and humidity setpoints and ramp rates
    try:
        new_temperature = int(input("Enter new temperature setpoint: "))
        new_humidity = int(input("Enter new humidity setpoint: "))

        # Ask for ramp rate in degrees per minute, but limit it to max allowed rate
        temp_ramp_rate = float(input(f"Enter temperature ramp rate (degrees per minute, max {MAX_TEMP_RAMP_RATE}): "))
        humidity_ramp_rate = float(input(f"Enter humidity ramp rate (percent per minute, max {MAX_HUMIDITY_RAMP_RATE}): "))

        # Ensure ramp rates do not exceed the maximum allowed
        if temp_ramp_rate > MAX_TEMP_RAMP_RATE:
            logger.warning(f"Temperature ramp rate cannot exceed {MAX_TEMP_RAMP_RATE} degrees per minute. Setting to {MAX_TEMP_RAMP_RATE}.")
            temp_ramp_rate = MAX_TEMP_RAMP_RATE

        if humidity_ramp_rate > MAX_HUMIDITY_RAMP_RATE:
            logger.warning(f"Humidity ramp rate cannot exceed {MAX_HUMIDITY_RAMP_RATE} percent per minute. Setting to {MAX_HUMIDITY_RAMP_RATE}.")
            humidity_ramp_rate = MAX_HUMIDITY_RAMP_RATE

        # Print current ramp rates
        logger.info(f"Current Temperature Ramp Rate: {temp_ramp_rate} degrees per minute")
        logger.info(f"Current Humidity Ramp Rate: {humidity_ramp_rate} percent per minute")

        # Step 3: Gradually change temperature
        if current_temperature < new_temperature:
            logger.info(f"Ramp up temperature from {current_temperature} to {new_temperature}...")
            while current_temperature < new_temperature:
                current_temperature += temp_ramp_rate
                if client.is_open:
                    client.write_single_register(temperature_register, int(current_temperature))
                logger.info(f"Current Temperature: {current_temperature:.2f}")
                time.sleep(60)  # Wait for one minute for the next increment
        elif current_temperature > new_temperature:
            logger.info(f"Ramp down temperature from {current_temperature} to {new_temperature}...")
            while current_temperature > new_temperature:
                current_temperature -= temp_ramp_rate
                if client.is_open:
                    client.write_single_register(temperature_register, int(current_temperature))
                logger.info(f"Current Temperature: {current_temperature:.2f}")
                time.sleep(60)  # Wait for one minute for the next increment

        # Step 4: Gradually change humidity
        if current_humidity < new_humidity:
            logger.info(f"Ramp up humidity from {current_humidity} to {new_humidity}...")
            while current_humidity < new_humidity:
                current_humidity += humidity_ramp_rate
                if client.is_open:
                    client.write_single_register(humidity_register, int(current_humidity))
                logger.info(f"Current Humidity: {current_humidity:.2f}")
                time.sleep(60)  # Wait for one minute for the next increment
        elif current_humidity > new_humidity:
            logger.info(f"Ramp down humidity from {current_humidity} to {new_humidity}...")
            while current_humidity > new_humidity:
                current_humidity -= humidity_ramp_rate
                if client.is_open:
                    client.write_single_register(humidity_register, int(current_humidity))
                logger.info(f"Current Humidity: {current_humidity:.2f}")
                time.sleep(60)  # Wait for one minute for the next increment

        logger.info(f"Successfully updated temperature to {new_temperature} and humidity to {new_humidity}")

    except ValueError as e:
        logger.error("Invalid input. Please enter valid integers or floats for temperature, humidity, and ramp rates.")
        logger.exception(e)
else:
    logger.error("Failed to read temperature or humidity from the PLC")

# Close the connection
logger.info("Closing the connection to the PLC.")
client.close()
