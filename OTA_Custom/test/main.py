#main stuff
import secretVars
import json
import time

with open("config.json",'r') as f:
    config = json.load(f)

print("main running")

def updater():
    import otacustom
    from machine import reset
    global config
    '''
    with open("config.json",'r') as f:
        config = json.load(f)
    '''
    checkList = []
    
    #global config
    updatePath = config["UPDATEPATH"]
    
    for index, files in enumerate(config['FILEMANIFEST']):
        ota_updater = otacustom.OTAUpdater(secretVars.ssid, secretVars.wifiPassword, updatePath, files['FILENAME'], files['VERSION'])
        newVersion = ota_updater.rolling_check_and_install()
        if newVersion:
            config["FILEMANIFEST"][index]["VERSION"] = newVersion
            config["FILEMANIFEST"][index]["CHECKFLAG"] = False
            checkList.append(True)
        else:
            config["FILEMANIFEST"][index]["CHECKFLAG"] = True
            checkList.append(False)
            
        del ota_updater
    
    if all(checkList):
        config["BOOTMODE"] == 0
    else:
        config["BOOTMODE"] == 1
        
    with open("config.json",'w') as f:
        json.dump(config, f)      
    
    return

updater()

time.sleep(2)

if config["BOOTMODE"] == 0:
    import logger
    #logger.main()
elif config["BOOTMODE"] == 1:
    machine.reset()
else:
    machine.reset()
        
        
    
    
        