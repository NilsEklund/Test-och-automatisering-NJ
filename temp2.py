import time

run = True

def run_print(input):
    global run
    run = input

def prints():
    counter = 0
    while run:
        print (counter)
        time.sleep(1)
        counter += 1