import pyvisa
import matplotlib.pyplot as plt
import datetime
from time import sleep

# -------------------------------------------------------------
# Block 1: Initialisera
# -------------------------------------------------------------

def initialisera():
    # Initialiserar anslutningen till oscilloskopet och returnerar instrumentobjektet
    rm = pyvisa.ResourceManager()

    # Hämta alla tillgängliga resurser för att identifiera oscilloskopet anslutet via USB
    resurser = rm.list_resources()
    print("Tillgängliga resurser:", resurser)

    # Kontrollera att resurser finns
    if not resurser:
        raise ValueError("Inga resurser hittades. Kontrollera anslutningen.")

    # Anslut till första resurser i listan, eller specificera rätt adress om flera finns
    # OBS! Instrumentadressen kan förstås hårdkodas med sin adress
    instrument_adress = resurser[0]
    oscilloskop = rm.open_resource(instrument_adress)

    # Kontrollera att vi är anslutna till rätt instrument genom att fråga om ID
    idn = oscilloskop.query('*IDN?')
    print(f"Ansluten till: {idn}")

    # Ställ in timeout och avslutning för kommunikation
    oscilloskop.timeout = 5000
    oscilloskop.write_termination = '\n'
    oscilloskop.read_termination = '\n'

    # Ofta behövs mer kod för att ställa in instrumentet inför mätning.
    # Exempel på ytterligare inställningar för oscilloskop är trig, kanal, tidsbas, ...
    # VIssa av dessa inställningar kan göras här, men man kan också behöva justera under mätningen.

    return oscilloskop

def read_raw_data(oscilloskop):
    try:
        # Sets vertical scale of channel 1 to 500mV
        oscilloskop.write('CH1:SCALE 0.5')
        # Sets time scale to 5ms
        oscilloskop.write('TIMEBASE:SCALE 5E-3')
        # Offcet channel 1 by 1.5 V
        oscilloskop.write('CH1:OFFSet 1.5')

        # Returns value of the time scale
        timebase_scale = oscilloskop.query('TIMEBASE:SCALE?')

        # Sets Trigger level to 2 volt
        oscilloskop.write('TRIGGER:EDGE:LEVELO 2.0')
        # Sets Trigger to channel 1
        oscilloskop.write('TRIGGER:EDGE:SOUR CH1')
        # Sets trigger to rising flank
        oscilloskop.write('TRIGGER:EDGE:SLOPe POSitive')

    except Exception as e:
        print(f'Failed to send command: {e}')

    sleep(3)

    try:
        # Trigger a singel sweap
        oscilloskop.write(':SINGLE')

        # Sets chanel 1 as data source
        oscilloskop.write(":WAV:SOUR CHAN1")
        # Sets mode to raw to measure the raw data
        oscilloskop.write(":WAV:MODE RAW")
        # Sets the format of the data to ASCII
        oscilloskop.write(":WAV:FORM ASCII")
        # Sends requiest to resive the raw data
        oscilloskop.write(":WAV:DATA?")

        # Resive the raw data
        raw_data = oscilloskop.read()

        # Sets mode to continuous mode
        oscilloskop.write(':RUN')
    
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

# -------------------------------------------------------------
# Huvudprogram
# -------------------------------------------------------------
def main():
    # Block 1: Initialisera
    try:
        oscilloskop = initialisera()
    except Exception as e:
        print(f"Initialisering misslyckades: {e}")
        return

    # Block 2: Mätning
    try:
        data = read_raw_data(oscilloskop)
    except Exception as e:
        print(f"Mätning misslyckades: {e}")
        return

    save_to_file(data[0], data[1])


    # Stäng anslutningen till oscilloskopet
    oscilloskop.close()

if __name__ == "__main__":
    main()
