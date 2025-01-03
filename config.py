# Modbus connection configuration
PLC_IP = '192.168.3.50'
PLC_PORT = 502

# Modbus Start/Stop Addresses
START_CHAMBER = 100 # Start Register
STOP_CHAMBER = 101 # Stop Register

# Register addresses
PARAMETER_MODBUS_ADDRESSES = {
    'Programmer.Run.Mode': 23,
    'Programmer.Run.PSP': 1,  # Temperature register
    'Programmer.Run.SegmentNumber': 56,
    'Programmer.Run.SegmentType': 29,
    'Programmer.Run.SegmentTimeLeft': 63
}

SEG_MODBUS_ADDRESSES = {
    'SEG_PTD_1[0]': 1,  # Humidity register
    'SEG_PTD_1[1]': 2,
    'SEG_PTD_1[2]': 3
}

# Operating limits
MIN_TEMPERATURE = -40
MAX_TEMPERATURE = 150
MIN_HUMIDITY = 20
MAX_HUMIDITY_TEMP = 80
MAX_HUMIDITY = 90


# Ramp rates
MAX_TEMP_RAMP_RATE = 5
MIN_TEMP_RAMP_RATE = 0
MAX_HUMIDITY_RAMP_RATE = 5
