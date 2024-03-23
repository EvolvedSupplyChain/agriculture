#web server for initial configuration of pico w
#import urequests as requests
import network
import socket
import time
import json
import machine

#def ap_mode(ssid, password):
ssid = 'viperSetup'
password = 'ganjagrower'
ap = network.WLAN(network.AP_IF)
ap.ifconfig('10.0.0.1', '255.255.255.0', '10.0.0.1', '10.0.0.1')
ap.config(essid=ssid, password=password, hostname='vipersetup')
ap.active(True)

while ap.active() == False:
    pass

print(ap.ifconfig())
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80))
s.listen(5)
    
def webpage():
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Viper Config</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Set up your new Viper:</h1>
            <form action="/setConfig", method="get">
            <label for="ssid">Wifi SSID:</label><br>
            <input type="text" id="ssid" name="ssid"><br>
            <label for="pw">Wifi Password:</label><br>
            <input type="text" id="pw" name="pw"><br>
            <p>
            <br>
            <label for="unitname">Name your Viper:</label><br>
            <input type="text" id="unitname" name="unitname"><br>
            <p>
            <br>
            <input type="radio" id="indoor" name="inout" value="indoor">
  			<label for="indoor">Indoor</label><br>
  			<input type="radio" id="outdoor" name="inout" value="outdoor">
            <label for="outdoor">Outdoor</label><br>
            <p>
            <br>
            <label for="plant1">Prefix name for your plants:</label><br>
            <input type="text" id="plant1" name="plant1"><br>
            <label for="plantnum">Number of plants:</label><br>
            <select id="plantnum" name="plantnum">
            	<option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
            </select>    
            <br>            
            <p>
            <br>
            <input type="submit" value="Submit">
            </form>

        </body>
        </html>

        """
    return str(html)

def qrpage():
    pass
    
#ap_mode("viperSetup","ganja")

def locatepage():
    pass

while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    request = str(request)
    print(request)
    #request = request.split()[1]
    if request.split()[1] == "/returnqr":
        #send the qr code page and a button to trigger the reset
        response = qrpage()
    elif request.split()[1] == "/setConfig":
        #write the config to file
        f = open('tempConfig.json','w')
        tempString = str(request.split()[1]).split('?')[1].split('&')
        tempList = []
        for x in tempString:
            tempList.append(x.split('='))
        tempDict = dict(tempList)
        json.dump(tempDict,f)
        f.close()                    
        #tempString = request.split()[1][request.split()[1].find('?')+1:]
        #tempString = tempString.split('&')
        #tempString = tempString.split('=')
        #tempDict = dict(tempString)
        #json.dump(tempDict,f)
        #f.close()
        
        response = locatepage()
        print(request)
    else:
        response = webpage()
    #response = web_page()
    conn.send(response)
    conn.close()

