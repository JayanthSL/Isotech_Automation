import time
from logger_setup import logger_config

logger = logger_config()

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
                time.sleep(60)
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
    
    def adjust_humidity(self, current_humidity, new_humidity, humidity_ramp_rate):
        """
        Gradually adjust the humidity to the desired setpoint.

        Args:
            current_humidity (float): The current humidity value.
            new_humidity (float): The target humidity setpoint.
            humidity_ramp_rate (float): The rate at which the humidity changes (percentage per minute).

        Steps:
            - Increments or decrements the humidity gradually.
            - Updates the humidity in the Modbus register after every step.
            - Waits for 60 seconds between steps to simulate real-world ramping.

        Note:
            If the current humidity equals the new humidity, no adjustment is made.
        """
        if current_humidity != new_humidity:
            logger.info(f"Adjusting humidity from {current_humidity} to {new_humidity}...")
            while current_humidity != new_humidity:
                time.sleep(60)
                step = humidity_ramp_rate if current_humidity < new_humidity else -humidity_ramp_rate
                current_humidity += step
                current_humiditys = max(min(new_humidity, current_humidity), min(current_humidity, new_humidity))
                self.client.write_register(self.humidity_register, int(current_humiditys))
                logger.info(f"Current Humidity: {current_humidity:.2f}")
                time.sleep(2)
        return current_humidity
