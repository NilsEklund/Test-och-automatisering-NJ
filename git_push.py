import subprocess

subprocess.call(['git','-C','/home/nils/Test-och-Automatisering-Data','add','data/'])
subprocess.call(['git','-C','/home/nils/Test-och-Automatisering-Data','commit','-m','new data'])
subprocess.call(['git','-C','/home/nils/Test-och-Automatisering-Data','push'])