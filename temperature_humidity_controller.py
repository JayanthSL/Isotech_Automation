import time
from loggerconfig import logger_config

logger = logger_config()

class TemperatureHumidityController:
    def __init__(self, modbus_client, temp_register, humidity_register):
        self.client = modbus_client
        self.temp_register = temp_register
        self.humidity_register = humidity_register
    
    def adjust_temperature(self, current_temperatureerature, new_temperature, temp_ramp_rate):
        if current_temperatureerature != new_temperature:
            logger.info(f"Adjusting temperature from {current_temperatureerature} to {new_temperature}...")
            while current_temperature != new_temperature:
                step = temp_ramp_rate if current_temperature < new_temperature else -temp_ramp_rate
                current_temperature += step
                current_temperature = max(min(new_temperature, current_temperature), min(current_temperature, new_temperature))
                self.client.write_register(self.temp_register, int(current_temperature))
                logger.info(f"Current Temperature: {current_temperature:.2f}")
                time.sleep(60)
        return current_temperature
    
    def adjust_humidity(self, current_humidity, new_humidity, humidity_ramp_rate):
        if current_humidity != new_humidity:
            logger.info(f"Adjusting humidity from {current_humidity} to {new_humidity}...")
            while current_humidity != new_humidity:
                step = humidity_ramp_rate if current_humidity < new_humidity else -humidity_ramp_rate
                current_humidity += step
                current_humidity = max(min(new_humidity, current_humidity), min(current_humidity, new_humidity))
                self.client.write_register(self.humidity_register, int(current_humidity))
                logger.info(f"Current Humidity: {current_humidity:.2f}")
                time.sleep(60)
        return current_humidity
