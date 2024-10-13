# Initiate communication with a the oscilloscope.
# Sends configuration commands to the oscilloscope.
# Reads the raw data from channel 1 of the oscilloscope.
# Saves the data in a new file named with current date and time

import pyvisa
import matplotlib.pyplot as plt
import datetime
from time import sleep

def initiate():
    # Initiating a connection to the oscilloscope and returns the instrument object.
    rm = pyvisa.ResourceManager()

    resources = rm.list_resources()
    print("Available resources:", resources)

    if not resources:
        raise ValueError("No resources found. Check the connection.")

    instrument_address = resources[0]
    oscilloscope = rm.open_resource(instrument_address)

    idn = oscilloscope.query('*IDN?')
    print(f"Connected to: {idn}")

    oscilloscope.timeout = 5000
    oscilloscope.write_termination = '\n'
    oscilloscope.read_termination = '\n'

    return oscilloscope

def read_raw_data(oscilloscope):
    try:
        # Sets vertical scale of channel 1 to 500mV
        oscilloscope.write('CH1:SCALE 0.5')
        # Sets time scale to 5ms
        oscilloscope.write('TIMEBASE:SCALE 5E-3')
        # Offset channel 1 by 1.5 V
        oscilloscope.write('CH1:OFFSet 1.5')

        # Returns value of the time scale
        timebase_scale = oscilloscope.query('TIMEBASE:SCALE?')

        # Sets Trigger level to 2 volt
        oscilloscope.write('TRIGGER:EDGE:LEVELO 2.0')
        # Sets Trigger to channel 1
        oscilloscope.write('TRIGGER:EDGE:SOUR CH1')
        # Sets trigger to rising flank
        oscilloscope.write('TRIGGER:EDGE:SLOPe POSitive')

    except Exception as e:
        print(f'Failed to send command: {e}')

    sleep(3)

    try:
        # Trigger a single sweep
        oscilloscope.write(':SINGLE')

        # Sets chanel 1 as data source
        oscilloscope.write(":WAV:SOUR CHAN1")
        # Sets mode to raw to measure the raw data
        oscilloscope.write(":WAV:MODE RAW")
        # Sets the format of the data to ASCII
        oscilloscope.write(":WAV:FORM ASCII")
        # Sends request to send the raw data
        oscilloscope.write(":WAV:DATA?")

        # Saves the raw data
        raw_data = oscilloscope.read()

        # Sets mode to continuous mode
        oscilloscope.write(':RUN')
    
    except Exception as e:
        print(f'Failed to read data: {e}')

    return raw_data, timebase_scale

def save_to_file(raw_data, time_scale):
    raw_data = raw_data.split(',')
    raw_data.pop(0)
    data = []
    data.append(float(time_scale))
    for data_point in raw_data:
        data.append(float(data_point))
    data = str(data)
    data = data.replace('[','')
    data = data.replace(']','')

    current_time = datetime.datetime.now()
    current_time = str(current_time)
    current_time = current_time.replace(' ','_')
    current_time = current_time.split('.')
    current_time = current_time[0].replace(':','.')
    file_path = '/home/nils/Test-och-Automatisering-Data/data/'
    filename = file_path +'test_' + current_time + '.csv'

    file = open(filename, mode = 'w')
    file.write(data)
    file.close()

def main():
    try:
        oscilloscope = initiate()
    except Exception as e:
        print(f"Initiation failed: {e}")
        return

    try:
        data = read_raw_data(oscilloscope)
    except Exception as e:
        print(f"Measuring : {e}")
        return

    save_to_file(data[0], data[1])

    oscilloscope.close()

if __name__ == "__main__":
    main()
