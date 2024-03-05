#import update
import os
import time
import gc
from ota import OTAUpdater
from machine import reset
from machine import Pin

#led = Pin("LED", Pin.OUT)
gc.collect()

g = open("updateFlag.txt","r+")
doUpdate = int(g.read())
#g.close()



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

if doUpdate == 1:
    firmware_url = "https://raw.githubusercontent.com/EvolvedSupplyChain/agriculture/main/"
    otaClient = OTAUpdater(secretVars.ssid, secretVars.wifiPassword, firmware_url, "logger.py")
    count = 0
    f.write(str(count))
    f.close()
    g.write(str(0))
    g.close()
    otaClient.download_and_install_update_if_available()
    
else:
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
