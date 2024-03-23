#import update
import os
import time

if "latest_code.py" in os.listdir():
    os.rename("latest_code.py", "logger.py")
    time.sleep(1)
    os.remove("latest_code.py")
    time.sleep(1)
else:
    pass
    
time.sleep(1)
    
import logger

logger.main()