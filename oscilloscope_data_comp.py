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

# -------------------------------------------------------------
# Block 2: Mätning
# -------------------------------------------------------------

def mata(oscilloskop):

    # Mät frekvensen från oscilloskopets mätfunktion
    try:
        oscilloskop.write(':AUToscale')
        # set-kommando:
        oscilloskop.write(':WAVeform:DATA')
        # query-kommando:
        raw_data = oscilloskop.query(':WAVeform:DATA?')
    except Exception as e:
        print(f"Misslyckades med att mäta frekvens: {e}")
    # Returnera den uppmätta frekvensen
    return raw_data

def read_raw_data(oscilloskop):
    try:
        #oscilloskop.write(':AUToscale')
        oscilloskop.write('CH1:SCALE 0.5')
        oscilloskop.write('TIMEBASE:SCALE 5E-3')
        oscilloskop.write('CH1:OFFSet 1.5')

        # Kontrollera om inställningarna är korrekt applicerade
        vertical_scale = oscilloskop.query('CH1:SCALE?')
        timebase_scale = oscilloskop.query('TIMEBASE:SCALE?')
        print (f'vertical_scale: {vertical_scale}')
        print (f'timebase_scale: {timebase_scale}')

        oscilloskop.write('TRIGGER:EDGE:LEVELO 2.0')  # Ställ in triggnivå på 2V
        oscilloskop.write('TRIGGER:EDGE:SOUR CH1')  # Trigga från kanal 1
        oscilloskop.write('TRIGGER:EDGE:SLOPe POSitive')  # Ställ in triggnivå för stigande flank

        sleep(1)

        oscilloskop.write('ACQUIRE:STATE ONCE')

        # Ställ in oscilloskopet för att mäta kanal 1 och ställ in vågformen som sinus
        oscilloskop.write(":WAV:SOUR CHAN1")  # Ställer in kanal 1 som datakälla
        oscilloskop.write(":WAV:MODE RAW")    # Hämtar rådata

        # Hämtar inställningar för att hämta vågformen
        oscilloskop.write(":WAV:FORM ASCII")  # Ställ in formatet för vågformsdata till ASCII
        oscilloskop.write(":WAV:DATA?")       # Begär vågformsdata från oscilloskopet

        # Hämta den råa vågformsdatan
        raw_data = oscilloskop.read()
    
    except Exception as e:
        print(f'Failed to read data: {e}')

    return raw_data

def save_to_file(raw_data):
    raw_data = raw_data.split(',')
    raw_data.pop(0)
    data = []
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

    save_to_file(data)


    # Stäng anslutningen till oscilloskopet
    oscilloskop.close()

if __name__ == "__main__":
    main()