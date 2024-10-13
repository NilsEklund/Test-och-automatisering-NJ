# Runs the git pull command for a specific git repo

import subprocess
from gpiozero import LED

blue_led = LED(15)

blue_led.on()

subprocess.call(['git','-C','/home/nils/Test-och-automatisering-NJ','pull'])

blue_led.off()