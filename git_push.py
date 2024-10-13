# Run all git command needed to push new files to a remote git repo

import subprocess
from gpiozero import LED

blue_led = LED(15)

blue_led.on()

subprocess.call(['git','-C','/home/nils/Test-och-Automatisering-Data','pull'])
subprocess.call(['git','-C','/home/nils/Test-och-Automatisering-Data','add','data/'])
subprocess.call(['git','-C','/home/nils/Test-och-Automatisering-Data','commit','-m','new data'])
subprocess.call(['git','-C','/home/nils/Test-och-Automatisering-Data','push'])

blue_led.off