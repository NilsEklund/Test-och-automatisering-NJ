import threading
from time import sleep
import pwm_test
import oscilloscope_data_comp
from gpiozero import LED

led = LED(14)

led.on()

pwm_thread = threading.Thread(target=pwm_test.pwm)
osc_thread = threading.Thread(target=oscilloscope_data_comp.main)

pwm_thread.start()
sleep(0.5)
osc_thread.start()

osc_thread.join()
pwm_test.run_pwm(False)
pwm_thread.join()

led.off()