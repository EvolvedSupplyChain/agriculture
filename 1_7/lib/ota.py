import network
import urequests
import os
import json
import machine
import itertools
from time import sleep

class OTAUpdater:
    """ This class handles OTA updates. It connects to the Wi-Fi, checks for updates, downloads and installs them."""
    def __init__(self, ssid, password, repo_url, filename):
        self.filename = filename
        self.ssid = ssid
        self.password = password
        self.repo_url = repo_url

        #self.version_url = repo_url + 'main/version.json'                 # Replacement of the version mechanism by Github's oid
        
        self.version_url = self.process_version_url(repo_url, filename)     # Process the new version url
        #self.firmware_url = repo_url + filename                             # Removal of the 'main' branch to allow different sources
        
        self.firmware_url = []
        for x in filname:
            self.firmware_url.append(self.version_url + x)

        # get the current version (stored in version.json)
        self.current_version = []
        
        if 'version.json' in os.listdir():    
            with open('version.json') as f:
                #tempList = json.load(f)
                
                #self.current_version = json.load(f)['version']
                self.current_version = json.load(f)['versions']
            print(f"Current device firmware version is '{self.current_version}'")

        else:
            #self.current_version = "0"
            dictList = []
            for x in filename:
                dictList.append(dict(file = x, version = "0"))
            # save the current version
            with open('version.json', 'w') as f:
                #json.dump({'version': self.current_version}, f)
                json.dump({'versions': dictList}, f)
            
    def process_version_url(self, repo_url, filename):
        """ Convert the file's url to its assoicatied version based on Github's oid management."""

        # Necessary URL manipulations
        '''
        version_url = repo_url.replace("raw.githubusercontent.com", "github.com")  # Change the domain
        version_url = version_url.replace("/", "§", 4)                             # Temporary change for upcoming replace
        version_url = version_url.replace("/", "/latest-commit/", 1)                # Replacing for latest commit
        version_url = version_url.replace("§", "/", 4)                             # Rollback Temporary change
        version_url = version_url + filename                                       # Add the targeted filename
        '''
        version_url = []
        
        for x in filename:
            tempversion_url = repo_url.replace("raw.githubusercontent.com", "github.com")  # Change the domain
            tempversion_url = tempversion_url.replace("/", "§", 4)                             # Temporary change for upcoming replace
            tempversion_url = tempversion_url.replace("/", "/latest-commit/", 1)                # Replacing for latest commit
            tempversion_url = tempversion_url.replace("§", "/", 4)                             # Rollback Temporary change
            tempversion_url = tempversion_url + x                                       # Add the targeted filename
            version_url.append(tempversion_url)
        
        return version_url

    def connect_wifi(self):
        """ Connect to Wi-Fi."""

        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(self.ssid, self.password)
        while not sta_if.isconnected():
            print('.', end="")
            sleep(0.25)
        print(f'Connected to WiFi, IP is: {sta_if.ifconfig()[0]}')
        
    def fetch_latest_code(self)->bool:
        """ Fetch the latest code from the repo, returns False if not found."""
        
        # Fetch the latest code from the repo.
        successList = []
        
        for x in self.firmware_url:
            response = urequests.get(x)
            if response.status_code == 200:
                print(f'Fetched latest firmware code, status: {response.status_code}, -  {response.text}')
    
                # Save the fetched code to memory
                self.latest_code = response.text
                try:
                    z = open(x[x.rfind("/")+1:len(x)-3] + 'New.py','w')
                    z.write(self.latest_code)
                    z.close()
                except Exception as error:
                    print(error)

                #return True
                successList.append(True)
        
            elif response.status_code == 404:
                print('Firmware not found.')
                successList.append(False)
                return False
        if all(successList):
            return True
        else:
            pass

    def update_no_reset(self):
        """ Update the code without resetting the device."""
        #todo: update this code to use version and file lists as well as the various "fileNew.py" files
        #instead of the "latest_code.py"

        # Save the fetched code and update the version file to latest version.
        with open('latest_code.py', 'w') as f:
            f.write(self.latest_code)
            sleep(1)
        # update the version in memory
        self.current_version = self.latest_version

        # save the current version
        with open('version.json', 'w') as g:
            json.dump({'version': self.current_version}, g)
        
        # free up some memory
        self.latest_code = None
        sleep(1)
        # Overwrite the old code.
        #os.rename('latest_code.py', self.filename)
        #os.rename('latest_code.py', 'logger.py')

    def update_and_reset(self):
        """ Update the code and reset the device."""
        #with open('latest_code.py', 'w') as f:
            #f.write(self.latest_code)
            
        print('Updating device...', end='')

        # Overwrite the old code.
        #os.rename('latest_code.py', self.filename)
        #os.rename('latest_code.py', 'logger.py')
        print(self.filename)
        

        # Restart the device to run the new code.
        print("Restarting device... (don't worry about an error message after this")
        sleep(0.25)
        machine.reset()  # Reset the device to run the new code.
        
    def check_for_updates(self):
        """ Check if updates are available."""
        
        # Connect to Wi-Fi
        self.connect_wifi()
        
        newerVersions = []
        
        for y in self.version_url:
            for z in self.current_version:
                if y[y.rfind("/")+1:] == z['file']:
                    #do the thing
                else:
                    pass
            #indent is wrong here, conform to if statements abovce
            print('Checking for latest version...')
            headers = {"accept": "application/json"} 
            response = urequests.get(y, headers=headers)
        
            data = json.loads(response.text)
            #print(data)
            self.latest_version = data['oid']                   # Access directly the id managed by GitHub
        
            print(f'latest version is: {self.latest_version}')
        
            # compare versions
            if self.current_version != self.latest_version:
                newerVersions.append(True)
            else:
                newerVersions.append(False)
                
            newer_version_available = True if any(newerVersions) else False
                    
            #newer_version_available = True if self.current_version != self.latest_version else False
        
            print(f'Newer version available: {newer_version_available}')    
        return newer_version_available
    
    def download_and_install_update_if_available(self):
        """ Check for updates, download and install them."""
        if self.check_for_updates():
            if self.fetch_latest_code():
                z = open('bootCount.txt','w')
                sleep(1)
                z.write("0")
                sleep(1)
                z.close()
                sleep(2)
                self.update_no_reset()
                self.update_and_reset()
        else:
            print('No new updates available.')
