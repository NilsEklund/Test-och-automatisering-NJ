import threading
from time import sleep
import pwm
import oscilloscope_data_comp
from gpiozero import LED

led = LED(14)

led.on()

pwm_thread = threading.Thread(target=pwm.pwm)
osc_thread = threading.Thread(target=oscilloscope_data_comp.main)

pwm_thread.start()
sleep(1)
osc_thread.start()

osc_thread.join()
pwm_thread.join()

led.off()