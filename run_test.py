import oscilloscope_data_comp
from gpiozero import LED

led = LED(17)

led.on()
oscilloscope_data_comp.main()
led.off()