import subprocess
from gpiozero import LED

led = LED(15)

led.on()

subprocess.call(['git','-C','/home/nils/Test-och-Automatisering-Data','pull'])
subprocess.call(['git','-C','/home/nils/Test-och-Automatisering-Data','add','data/'])
subprocess.call(['git','-C','/home/nils/Test-och-Automatisering-Data','commit','-m','new data'])
subprocess.call(['git','-C','/home/nils/Test-och-Automatisering-Data','push'])

led.off