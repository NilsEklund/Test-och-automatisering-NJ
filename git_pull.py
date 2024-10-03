import subprocess
from gpiozero import LED

led = LED(10)

led.on()

subprocess.call(['git','-C','/home/nils/Test-och-automatisering-NJ','pull'])

led.off()