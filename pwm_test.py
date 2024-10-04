from gpiozero import LED
import time

led = LED(13)

run = True

def run_pwm(input):
    global run
    run = input

def pwm():
    while run:
        led.on()
        time.sleep(0.01)
        led.off()
        time.sleep(0.01)