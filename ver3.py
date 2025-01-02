import time
from modbus_client import ModbusServerHandler
from logger_setup import logger_config
from config import (PLC_IP, PLC_PORT, START_CHAMBER, STOP_CHAMBER, PARAMETER_MODBUS_ADDRESSES, SEG_MODBUS_ADDRESSES,
                    MIN_TEMPERATURE, MAX_TEMPERATURE, MIN_HUMIDITY, MAX_HUMIDITY_TEMP, MAX_HUMIDITY,
                    MAX_TEMP_RAMP_RATE, MIN_TEMP_RAMP_RATE, MAX_HUMIDITY_RAMP_RATE)

logger = logger_config()

modbus_client = ModbusServerHandler(PLC_IP, PLC_PORT)

class TemperatureHumidityController:
    """
    A controller to adjust and monitor temperature and humidity using Modbus communication.
    """
    def __init__(self, modbus_client, temp_register, humidity_register):
        """
        Initialize the controller with Modbus client and register addresses.

        Args:
            modbus_client: The Modbus client instance used for communication.
            temp_register: Modbus register address for temperature.
            humidity_register: Modbus register address for humidity.
        """
        self.client = modbus_client
        self.temp_register = temp_register
        self.humidity_register = humidity_register
    
    def adjust_temperature(self, current_temperature, new_temperature, temp_ramp_rate):
        """
        Gradually adjust the temperature to the desired setpoint.

        Args:
            current_temperature (float): The current temperature value.
            new_temperature (float): The target temperature setpoint.
            temp_ramp_rate (float): The rate at which the temperature changes (degrees per minute).

        Steps:
            - Increments or decrements the temperature gradually.
            - Updates the temperature in the Modbus register after every step.
            - Waits for 60 seconds between steps to simulate real-world ramping.

        Note:
            If the current temperature equals the new temperature, no adjustment is made.
        """
        if current_temperature != new_temperature:
            logger.info(f"Adjusting temperature from {current_temperature} to {new_temperature}...")
            while current_temperature != new_temperature:
                # time.sleep(60)
                step = temp_ramp_rate 
                current_temperature += step
                print(current_temperature, "Current Temp")
                current_new_temperature = step
                print("New", current_new_temperature)
                current_temperatures = max(min(new_temperature, current_temperature), min(current_temperature, new_temperature))
                # current_temperature = max(min(new_temperature, current_temperature), min(current_temperature, new_temperature))
                self.client.write_register(self.temp_register, int(current_temperatures))
                logger.info(f"Current Temperature: {current_temperature:.2f}")
                time.sleep(2)
        return current_temperature
    
    def adjust_humidity(self, current_humidity, new_humidity):
        """
        Gradually adjust the humidity to the desired setpoint.

        Args:
            current_humidity (float): The current humidity value.
            new_humidity (float): The target humidity setpoint.

        Steps:
            - Increments or decrements the humidity gradually.
            - Updates the humidity in the Modbus register after every step.

        Note:
            If the current humidity equals the new humidity, no adjustment is made.
        """
        if current_humidity != new_humidity:
            logger.info(f"Adjusting humidity from {current_humidity} to {new_humidity}...")
            while current_humidity != new_humidity:
                current_humidity = new_humidity
                self.client.write_register(self.humidity_register, int(current_humidity))
                logger.info(f"Current Humidity: {current_humidity:.2f}")
                time.sleep(1)
        return current_humidity

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
    start = modbus_client.read_register(START_CHAMBER)

    if temperature and humidity and start:
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
            print(new_temperature, "new humidity")
            if new_temperature < MIN_HUMIDITY or new_temperature > MAX_HUMIDITY_TEMP:
                new_humidity = 0
                break
            else:
                try:
                    new_humidity = int(input(f"Enter new humidity setpoint ({MIN_HUMIDITY} to {MAX_HUMIDITY}): "))
                    if not (MIN_HUMIDITY <= new_humidity <= MAX_HUMIDITY):
                        print(new_humidity, "new humidity")
                        logger.error(f"Humidity setpoint must be between {MIN_HUMIDITY} and {MAX_HUMIDITY}.")
                        print("Please try again.\n")
                        continue  # Loop back to re-enter humidity
                    break  # Exit loop if input is valid

                except ValueError:
                    logger.error("Invalid input. Please enter a valid integer for humidity.")
                    print("Please try again.\n")

        while True:
            try:
                # Ask user for the time taken to increase the temperature
                time_minutes = float(input(f"Enter the time (in minutes) to increase temperature from {current_temperature} to {new_temperature}: "))
                
                if time_minutes <= 0:
                    logger.error("Invalid time. Please enter a positive value greater than 0.")
                    print("Please try again.\n")
                    continue  # Loop back to the input field

                # Calculate the ramp rate
                temperature_change = new_temperature - current_temperature  # Change in temperature (10°C)
                temp_ramp_rate = temperature_change / time_minutes  # Ramp rate (degrees per minute)
                
                print(temp_ramp_rate, "Hello")

                temp_ramp_rates = abs(temp_ramp_rate)  # Converts the negative value to positive
                print(temp_ramp_rates)

                # Validate the ramp rate against the maximum allowed value
                if temp_ramp_rates > MAX_TEMP_RAMP_RATE or temp_ramp_rates < MIN_TEMP_RAMP_RATE:
                    logger.error(f"Calculated ramp rate ({temp_ramp_rate:.2f}°C/min) exceeds the maximum allowed rate of {MAX_TEMP_RAMP_RATE}°C/min.")
                    print("Please enter a longer time duration.\n")
                    continue  # Loop back to the input field

                # Valid input and ramp rate
                logger.info(f"Valid ramp rate calculated: {temp_ramp_rate:.2f}°C/min")
                print(f"Ramp rate successfully set to {temp_ramp_rate:.2f}°C/min.")
                break  # Exit loop when input is valid

            except ValueError:
                logger.error("Invalid input. Please enter a numerical value.")
                print("Please try again.\n")

        # Adjust temperature and humidity
        current_temperature = controller.adjust_temperature(current_temperature, new_temperature, temp_ramp_rate)
        current_humidity = controller.adjust_humidity(current_humidity, new_humidity)

        logger.info(f"Successfully updated temperature to {new_temperature} and humidity to {new_humidity}.")
        return main()
    
    else:
        logger.error("Failed to read temperature or humidity from the PLC.")
        return main()
    
def main():
    """
    Displays the main menu for controlling temperature and humidity.
    Allows the user to choose between adjusting settings or exiting the program.
    """
    print("\n=== Temperature and Humidity Control Menu ===")
    print("1. Adjust Temperature and Humidity")
    print("2. Exit")
    
    try:
        choice = int(input("Enter your choice (1-2): "))
        if choice == 1:
            temperature_humity_control()
        elif choice == 2:
            print("Exiting the program. Goodbye!")
            exit(0)
        else:
            print("Invalid choice. Please select a valid option.")
            main()  # Re-display the menu for invalid input
    except ValueError:
        print("Invalid input. Please enter a numerical value.")
        main()  # Re-display the menu for invalid input

if __name__ == "__main__":
    controller = TemperatureHumidityController(
        modbus_client,
        PARAMETER_MODBUS_ADDRESSES['Programmer.Run.PSP'],
        SEG_MODBUS_ADDRESSES['SEG_PTD_1[1]']
    )
    main()
