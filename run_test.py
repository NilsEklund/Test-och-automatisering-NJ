# Starts a new test

import threading
from time import sleep
import pwm
import oscilloscope_com
from gpiozero import LED

red_led = LED(14)

red_led.on()

pwm_thread = threading.Thread(target=pwm.run_pwm)
osc_thread = threading.Thread(target=oscilloscope_com.main)

pwm_thread.start()
sleep(1)
osc_thread.start()

osc_thread.join()
pwm.stop_pwm(False)
pwm_thread.join()

red_led.off()