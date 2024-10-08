import threading
from time import sleep
import pwm_new
import oscilloscope_data_comp
from gpiozero import LED

led = LED(14)

led.on()

pwm_thread = threading.Thread(target=pwm_new.run_pwm)
osc_thread = threading.Thread(target=oscilloscope_data_comp.main)

pwm_thread.start()
sleep(1)
osc_thread.start()

osc_thread.join()
pwm_new.stop_pwm(False)
pwm_thread.join()

led.off()