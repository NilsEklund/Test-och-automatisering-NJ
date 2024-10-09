import RPi.GPIO as GPIO
import time
import math

run = True

def stop_pwm(input):
    global run
    run = input

def run_pwm():
    # Setup GPIO
    GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
    pwm_pin = 18            # Set the pin for PWM (GPIO 18 as example)
    GPIO.setup(pwm_pin, GPIO.OUT)

    # Set PWM frequency (50 Hz)
    pwm_frequency = 2500  # You want to create a 50 Hz wave, but high PWM frequency for smoother output
    pwm = GPIO.PWM(pwm_pin, pwm_frequency)
    pwm.start(0)  # Start PWM with 0% duty cycle

    # Parameters
    wave_frequency = 150  # 50 Hz sine wave
    steps = 200          # Number of steps per wave period
    delay = 1.0 / (wave_frequency * steps)  # Time delay per step to match 50 Hz wave


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