# Creates a PWM signal to recreate a sin wave using a LP filter.
# Stops PWM signal when stop_pwm is called

import RPi.GPIO as GPIO
import time
import math

run = True

def stop_pwm(input):
    global run
    run = input

def run_pwm():
    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    pwm_pin = 18
    GPIO.setup(pwm_pin, GPIO.OUT)

    # Set PWM frequency (50 Hz)
    pwm_frequency = 2500
    pwm = GPIO.PWM(pwm_pin, pwm_frequency)
    # Set PWM duty cycle to start at 0%
    pwm.start(0)

    # Parameters
    wave_frequency = 150
    steps = 200
    delay = 1.0 / (wave_frequency * steps)

    while run:
        for step in range(steps):
            # Calculate the angle for the sine wave (0 to 2pi)
            angle = 2 * math.pi * step / steps
            # Calculate the sine value and convert it to a duty cycle (0 to 100%)
            duty_cycle = (math.sin(angle) + 1) * 50  # Sine wave range is -1 to 1, convert to 0 to 100%
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(delay)  # Wait for the next step


    pwm.stop()
    GPIO.cleanup()

if __name__ == '__main__': 
   run_pwm()
   