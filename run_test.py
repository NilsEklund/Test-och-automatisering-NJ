import oscilloscope_data_comp
from gpiozero import LED

led = LED(14)

led.on()
oscilloscope_data_comp.main()
led.off()