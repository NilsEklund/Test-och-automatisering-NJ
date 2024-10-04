import RPi.GPIO as GPIO
import numpy as np
import time

def pwm():
    # GPIO setup
    GPIO.setmode(GPIO.BCM)  # Använd BCM-nummer
    pin = 13  # GPIO 13 motsvarar fysiska pinne 33
    GPIO.setup(pin, GPIO.OUT)

    # PWM setup
    pwm_frequency = 1000  # PWM frekvens i Hz
    pwm = GPIO.PWM(pin, pwm_frequency)  # Initiera PWM på pinne 13
    pwm.start(0)  # Starta PWM med 0% duty cycle

    # Parametrar
    sin_frequency = 50  # 50 Hz sinusvåg
    sampling_rate = pwm_frequency * 20  # Samplingsfrekvens
    duration = 5  # Kör programmet i 15 sekunder

    # Generera sinusvågen
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    sin_wave = 0.5 * (1 + np.sin(2 * np.pi * sin_frequency * t))  # Normalisera mellan 0 och 1

    # Skicka ut PWM signalen
    try:
        for value in sin_wave:
            duty_cycle = value * 100  # Konvertera till % (mellan 0 och 100)
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(1 / sampling_rate)  # Vänta tills nästa sampling

    finally:
        pwm.stop()  # Stanna PWM
        GPIO.cleanup()  # Rensa GPIO inställningar

