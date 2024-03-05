#import update
import os
import time
import gc
from machine import reset
from machine import Pin

#led = Pin("LED", Pin.OUT)
gc.collect()


f = open('bootCount.txt','r')
time.sleep(3)
count = int(f.read())
time.sleep(2)
print(count)
f.close()
time.sleep(3)
f = open('bootCount.txt','w')
time.sleep(1)

'''    
#f.close()
time.sleep(1)
led.on()
time.sleep(1)
led.off()
time.sleep(1)
led.on()
time.sleep(1)
led.off()
'''
print(count)

#f = open('bootCount.txt','w')

if 'latest_code.py' in os.listdir():
    #f = open("bootCount.txt",'w')
    #f.write(
    os.remove('logger.py')
    time.sleep(3)
    os.rename('latest_code.py', 'logger.py')
    time.sleep(3)
    #os.remove('latest_code.py')
    #time.sleep(3)
    #f = open('bootCount.txt','w')
    time.sleep(3)
    f.write("0")
    time.sleep(3)
    f.close()
    time.sleep(5)
    machine.reset()
else:
    if count < 2:
        print(count)
        count = count + 1
        print(count)
        #f = open('bootCount.txt','w')
        time.sleep(3)
        f.write(str(count))
        time.sleep(5)
        f.close()
        time.sleep(5)
        #print(count)
        machine.reset()
        
    else:
        f.write("0")
        time.sleep(3)
        f.close()
        #os.remove('bootCount.txt')
        time.sleep(5)    
        import logger
        time.sleep(5)
        #logger.main()