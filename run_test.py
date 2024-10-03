import oscilloscope_data_comp
from gpiozero import LED

led = LED(8)

led.on()
oscilloscope_data_comp.main()
led.off()