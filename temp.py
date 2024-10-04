import threading
import time
import temp2



def timer ():
    for i in range(0,11):
        time.sleep(1)
    print('stop')

t = threading.Thread(target=temp2.prints)
t2 = threading.Thread(target=timer)

t.start()
t2.start()

t2.join()
temp2.run_print(False)
t.join()