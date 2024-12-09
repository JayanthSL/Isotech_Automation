from pyModbusTCP.client import ModbusClient

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

# Step 1: Read the current temperature and humidity from the PLC
temperature = client.read_holding_registers(1,1)
humidity = client.read_holding_registers(2,1)

if temperature and humidity:
    current_temperature = temperature[0]
    current_humidity = humidity[0]
    print(f"Current Temperature: {current_temperature}")
    print(f"Current Humidity: {current_humidity}")

    # Step 2: Prompt user for new temperature and humidity setpoints
    try:
        new_temperature = int(input("Enter new temperature setpoint: "))
        new_humidity = int(input("Enter new humidity setpoint: "))

        # Step 3: Write the new temperature setpoint to the PLC
        print(f"Writing to temperature register at address {temperature_register} with value {new_temperature}")
        if client.is_open and client.write_single_register(temperature_register, new_temperature):
            print(f"Successfully updated temperature to {new_temperature}")
        else:
            print("Failed to update temperature")

        # Step 4: Write the new humidity setpoint to the PLC
        print(f"Writing to humidity register at address {humidity_register} with value {new_humidity}")
        if client.is_open and client.write_single_register(humidity_register, new_humidity):
            print(f"Successfully updated humidity to {new_humidity}")
        else:
            print("Failed to update humidity")

    except ValueError:
        print("Invalid input. Please enter valid integers for temperature and humidity.")
else:
    print("Failed to read temperature or humidity from the PLC")

# Close the connection
client.close()

