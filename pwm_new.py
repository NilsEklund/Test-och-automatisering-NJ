import RPi.GPIO as GPIO
import time
import numpy as np

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
soft_pwm = GPIO.PWM(40, 10000)

def setup():
    soft_pwm.start(0)

def loop():
    for dc in range(0, 100, 1):
        soft_pwm.ChangeDutyCycle(dc)
        time.sleep(0.00001)
    for dc in range (100, 0, -1):
        soft_pwm.ChangeDutyCycle(dc)
        time.sleep(0.000001)

data_points = 2000

def loop_2():
    for i in range(0, data_points):

        x = i / data_points

        dc = 45 * np.sin(2 * np.pi * x) + 45

        soft_pwm.ChangeDutyCycle(dc)
       # time.sleep(0.00001)


def endprogram():
    soft_pwm.stop()
    GPIO.cleanup()

if __name__ == '__main__':
    setup()

    while True:
        try:
            loop_2()
        except KeyboardInterrupt:
            print('Stop')
            endprogram()
            break

run = True

def stop_pwm(input):
    global run
    run = input

def run_pwm():
    setup()

    while run:
        loop()
