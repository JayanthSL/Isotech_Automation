from modbus_client import ModbusServerHandler
from chamber_control import ChamberControl
from climate_controller import TemperatureHumidityController
from logger_setup import logger_config
from settings import (PLC_IP, PLC_PORT, START_CHAMBER, STOP_CHAMBER, PARAMETER_MODBUS_ADDRESSES, SEG_MODBUS_ADDRESSES,
                    MIN_TEMPERATURE, MAX_TEMPERATURE, MIN_HUMIDITY, MAX_HUMIDITY,
                    MAX_TEMP_RAMP_RATE, MAX_HUMIDITY_RAMP_RATE)

# Configure logger
logger = logger_config()

# Connect to Siemens PLC
modbus_client = ModbusServerHandler(PLC_IP, PLC_PORT)

#Initiating Chamber Controls
chamber_control = ChamberControl(modbus_client, START_CHAMBER, STOP_CHAMBER)

# Create controller for temperature and humidity
controller = TemperatureHumidityController(modbus_client, 
                                           PARAMETER_MODBUS_ADDRESSES['Programmer.Run.PSP'], 
                                           SEG_MODBUS_ADDRESSES['SEG_PTD_1[1]'])

if not modbus_client.client.is_open:
    logger.error("Failed to connect to the PLC. Please check the connection.")
    exit()

def temperature_humity_control():
    """
    Controls temperature and humidity for the chamber.
    - Reads the current temperature and humidity from the PLC.
    - Prompts the user to input new setpoints and ramp rates.
    - Adjusts temperature and humidity gradually based on input.
    """
    logger.info("Reading current temperature and humidity from the PLC.")
    temperature = modbus_client.read_register(PARAMETER_MODBUS_ADDRESSES['Programmer.Run.PSP'])
    humidity = modbus_client.read_register(SEG_MODBUS_ADDRESSES['SEG_PTD_1[1]'])

    if temperature and humidity:
        current_temperature = temperature[0]
        current_humidity = humidity[0]
        logger.info(f"Current Temperature: {current_temperature}")
        logger.info(f"Current Humidity: {current_humidity}")

        
        while True:
            try:
                new_temperature = int(input(f"Enter new temperature setpoint ({MIN_TEMPERATURE} to {MAX_TEMPERATURE}): "))
                if not (MIN_TEMPERATURE <= new_temperature <= MAX_TEMPERATURE):
                    logger.error(f"Temperature setpoint must be between {MIN_TEMPERATURE} and {MAX_TEMPERATURE}.")
                    print("Please try again.\n")
                    continue  # Loop back to re-enter temperature
                break  # Exit loop if input is valid
            except ValueError:
                logger.error("Invalid input. Please enter a valid integer for temperature.")
                print("Please try again.\n")

        while True:
            try:
                new_humidity = int(input(f"Enter new humidity setpoint ({MIN_HUMIDITY} to {MAX_HUMIDITY}): "))
                if not (MIN_HUMIDITY <= new_humidity <= MAX_HUMIDITY):
                    logger.error(f"Humidity setpoint must be between {MIN_HUMIDITY} and {MAX_HUMIDITY}.")
                    print("Please try again.\n")
                    continue  # Loop back to re-enter humidity
                break  # Exit loop if input is valid
            except ValueError:
                logger.error("Invalid input. Please enter a valid integer for humidity.")
                print("Please try again.\n")


        while True:
            try:
                temp_ramp_rate = float(input(f"Enter temperature ramp rate (degrees per minute, max {MAX_TEMP_RAMP_RATE}): "))
                if temp_ramp_rate > MAX_TEMP_RAMP_RATE or temp_ramp_rate < MAX_TEMP_RAMP_RATE:
                    logger.error(f"Invalid temperature ramp rate. Must be {MAX_TEMP_RAMP_RATE}.")
                    print("Please try again.\n")
                    continue  # Loop back to the input field
                break  # Exit loop when input is valid
            except ValueError:
                logger.error("Invalid input. Please enter a numerical value.")
                print("Please try again.\n")

        while True:
            try:
                humidity_ramp_rate = float(input(f"Enter humidity ramp rate (percent per minute, max {MAX_HUMIDITY_RAMP_RATE}): "))
                if humidity_ramp_rate > MAX_HUMIDITY_RAMP_RATE or humidity_ramp_rate < MAX_HUMIDITY_RAMP_RATE:
                        logger.error(f"Invalid humidity ramp rate. Must be {MAX_HUMIDITY_RAMP_RATE}.")
                        print("Please try again.\n")
                        continue  # Loop back to the input field
                break  # Exit loop when input is valid
            except ValueError:
                logger.error("Invalid input. Please enter a numerical value.")
                print("Please try again.\n")


        # Adjust temperature and humidity
        current_temperature = controller.adjust_temperature(current_temperature, new_temperature, temp_ramp_rate)
        current_humidity = controller.adjust_humidity(current_humidity, new_humidity, humidity_ramp_rate)

        logger.info(f"Successfully updated temperature to {new_temperature} and humidity to {new_humidity}.")
        return main()
    
    else:
        logger.error("Failed to read temperature or humidity from the PLC.")
        return main()

def main():
    """
    Main function to manage chamber operations.
    - Provides options to start/stop chamber or control temperature and humidity.
    - Loops until the user exits the program.
    """
    while True:
        print("Chamber Control And Monitoring System")
        print("1. Start Chamber")
        print("2. Stop Chamber")
        print("3. Control Temperature and Humidity")
        print("4. Exit")

        choice = int(input("Enter Your Choise:"))

        if choice == 1:
            chamber_control.start_chamber()
        elif choice == 2:
            chamber_control.stop_chamber()
        elif choice == 3:
            temperature_humity_control()
        elif choice == 4:
            logger.info(f"Exiting program, Closing connection with PLC")
            modbus_client.close_connection()
            break
        else:
            logger.error(f"Invalid Choice, Please enter the Valid option")

if __name__ == "__main__":
    main()  