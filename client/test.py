import threading
from time import sleep

result = 0
    

def boo():
    print("start boo")
    global result 
    result += 1
    print("end boo")

t1 = threading.Thread(target=boo)
t1.run()

print("adwwada")
sleep(1)
if t1.is_alive()

