import utime
import time
import bmp280
import aht10
import onewire
import ds18x20
import as7265x
import TSL2591
import network
import socket
import secretVars
import ubinascii
import json
import gc
import struct
from umqttsimple import MQTTClient
from ota import OTAUpdater
from machine import Pin, SPI, I2C, ADC
#from Arducam import *
#from camera import *

'''wifi connection:'''
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(secretVars.ssid, secretVars.wifiPassword)

while station.isconnected() == False:
    pass
print(station.ifconfig())


'''Time Check and Clock Set:'''
NTP_DELTA = 2208988800   #Adjust this for time zone
timeHost = "pool.ntp.org"
rtClock = machine.RTC()

def set_time():
    # Get the external time reference
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(host, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()

    #Set our internal time
    val = struct.unpack("!I", msg[40:44])[0]
    tm = val - NTP_DELTA    
    t = time.gmtime(tm)
    rtc.datetime((t[0],t[1],t[2],t[6]+1,t[3],t[4],t[5],0))


'''OTA Updater'''
firmware_url = "https://raw.githubusercontent.com/EvolvedSupplyChain/agriculture/main"
updateFile = "main.py"
updateFilesList = []

otaClient = OTAUpdater(secretVars.ssid, secretVars.wifiPassword, firmware_url, "main.py")
#otaClient = OTAUpdater(secretVars.ssid, secretVars.wifiPassword, firmware_url, updateFile)
#otaClient.download_and_install_update_if_available()


'''MQTT:'''

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == secretVars.ccTopic:
    print('Topic: ' + topic + 'Message: ' + msg)
    match msg:
        case "setProp":
            print(msg)
        case "reboot":
            print(msg)
        case _:
            print(msg)
            #parse the incoming JSON and extract some "messageType" variable, take appropriate action 
        
  else:
    print('message recieved: ' + msg)

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(secretVars.clientID, secretVars.brokerAddress, keepalive=60)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(secretVars.ccTopic)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (secretVars.brokerAddress, secretVars.ccTopic))
  return client

client = connect_and_subscribe()


'''ambient temp, humidity, and pressure sensors:'''
ambientPower = Pin(22, Pin.OUT)
ambientPower.value(1)
time.sleep(1)
ambientI2CBus = I2C(0,scl=Pin(1),sda=Pin(0))
time.sleep(2)
tempHum = aht10.AHT10(ambientI2CBus)
time.sleep(2)
tempPres = bmp280.BMP280(ambientI2CBus)
time.sleep(2)
tempPres.use_case(bmp280.BMP280_CASE_INDOOR)
time.sleep(2)

'''spectral and lux sensors:'''
lightPower = Pin(20, Pin.OUT)
lightPower.value(1)
time.sleep(3)
spectralI2CBus = I2C(1,scl=Pin(7),sda=Pin(6))
time.sleep(3)
specTriad = as7265x.AS7265X(spectralI2CBus)
time.sleep(3)
specTriad.disable_indicator()
time.sleep_ms(500)
specTriad.disable_bulb(as7265x.AS7265x_LED_WHITE)
specTriad.disable_bulb(as7265x.AS7265x_LED_IR)
specTriad.disable_bulb(as7265x.AS7265x_LED_UV)
time.sleep_ms(500)
#specTriad.set_measurement_mode(as7265x.AS7265X_MEASUREMENT_MODE_6CHAN_CONTINUOUS)
#specTriad.begin()
#specTriad.disableBulb(as7265x.LED_WHITE)
#specTriad.disableBulb(as7265x.LED_IR)
#specTriad.disableBulb(as7265x.LED_UV)
#luxSense = tsl2591.Tsl2591(spectralI2CBus)
luxSense = TSL2591.TSL2591(spectralI2CBus)

'''temp and moisture probes:'''
tempProbeData = Pin(2)
tempProbePower = Pin(3, Pin.OUT)
tempProbePower.value(1)
#moistureProbeData = Pin(4, Pin.IN)
moistureProbeDataPin = Pin(26, Pin.IN)
moistureProbeData = ADC(moistureProbeDataPin)
offsetPin = ADC(Pin(27, Pin.IN))

#moistureProbeData = ADC(0)

moistureProbePower = Pin(21,Pin.OUT)
moistureProbePower.value(1)

'''Camera:'''

#take_image()
time.sleep(3)


'''
mode = 0
start_capture = 0
stop_flag=0
once_number=128
value_command=0
flag_command=0
buffer=bytearray(once_number)
#imageSense = ArducamClass(OV5642)
imageSense = ArducamClass(OV5642)
time.sleep(1)
imageSense.Camera_Detection()
time.sleep(1)
imageSense.Spi_Test()
time.sleep(1)
imageSense.Camera_Init()
time.sleep(1)
imageSense.Spi_write(ARDUCHIP_TIM,VSYNC_LEVEL_MASK)
utime.sleep(2)
imageSense.clear_fifo_flag()
time.sleep(1)
imageSense.Spi_write(ARDUCHIP_FRAMES,0x00)
time.sleep(1)

#global imageBuff
#imageBuff = []
def read_fifo_burst():
    count=0
    lenght=imageSense.read_fifo_length()
    imageSense.SPI_CS_LOW()
    imageSense.set_fifo_burst()
    #global imageBuff
    #imageBuff=[]
    
    try:
        with open("imageTemp.byte", 'wb') as f:
            f.write(buffer)
    except:
        print("errrooooorrrrrr!")
    
    #f = open("imageTemp.byte",'w')
    while True:
        imageSense.spi.readinto(buffer,start=0,end=once_number)
        #f = open("imageTemp.txt",'w')
        #f.write(buffer)
        #f.close()
        #usb_cdc.data.write(buffer)
        #time.sleep_ms(20)
        #imageBuff.append(buffer)
        #print(buffer)
        
        utime.sleep(0.00015)
        count+=once_number
        if count+once_number>lenght:
            count=lenght-count
            imageSense.spi.readinto(buffer,start=0,end=count)
            #f = open("imageTemp.txt",'a')
            #f.write(buffer) 
            #f.close()
            #time.sleep_ms(20)
            #imageBuff.append(buffer)
            #print(imageBuff)
            #print(buffer)
            #usb_cdc.data.write(buffer)
            imageSense.SPI_CS_HIGH()
            imageSense.clear_fifo_flag()
            break
    #print(buffer)
    #print(imageBuff)
    #f.close()    
    '''


'''analog data mapping function:'''
def convert(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

'''update call'''
#run the RTC NTP update
#open a text file with logs of previous updates and update checks
#compare last update check time from file to clock
#run updater if needed, log details and close the file
#collect garbage

#listen on MQTT command channel for forced update

'''main program:'''
def main():
    
    #run the updater
    otaClient.download_and_install_update_if_available()
    #check for MQTT messages
    
    
    #check the clock and compare to update flag, run update function if needed
    
    tempBus = ds18x20.DS18X20(onewire.OneWire(tempProbeData))
    temps = tempBus.scan()
    
    while True:
        soilMoist = 0
        tempList = []
        tempBus.convert_temp()
        time.sleep_ms(800)
        for i in temps:
            tempList.append(tempBus.read_temp(i))
        
        #ambientData = [0,tempPres.temperature,tempPres.pressure,0]
        
        #ambientData = [tempHum.temperature(),tempPres.temperature,tempPres.pressure,tempHum.humidity()]
        ambientData = [tempHum.temperature(),tempPres.temperature,tempPres.pressure,tempHum.humidity(),tempHum.dew_point()]
        
        
        #moistureProbePower.value(1)
        time.sleep(2)
        soilMoist = moistureProbeData.read_u16()
        offsetReading = offsetPin.read_u16()
        time.sleep_ms(500)
        print(soilMoist)
        print(offsetReading)
        
        soilMoist = soilMoist - offsetReading
        
        soilMoist = soilMoist * 3.2 / 65535
        #moistureProbePower.value(0)
        #soilMoist = soilMoist * (3.3 / 65535) 
        #soilMoist = (3.3 - soilMoist) / 3.3 * 100
        #soilMoist = convert(soilMoist, 0, 65535, 100, 0)
        
        
        
        #fullLux, irLux = luxSense.get_full_luminosity()
        #totalLux = luxSense.calculate_lux(fullLux, irLux)
        fullLux = [luxSense.lux, luxSense.infrared, luxSense.visible, luxSense.full_spectrum]
        
        
        specTriad.take_measurements()
        specData = []
        specData.append(specTriad.get_calibrated_A())
        specData.append(specTriad.get_calibrated_B())
        specData.append(specTriad.get_calibrated_C())
        specData.append(specTriad.get_calibrated_D())
        specData.append(specTriad.get_calibrated_E())
        specData.append(specTriad.get_calibrated_F())
        specData.append(specTriad.get_calibrated_G())
        specData.append(specTriad.get_calibrated_H())
        specData.append(specTriad.get_calibrated_R())        
        specData.append(specTriad.get_calibrated_I())
        specData.append(specTriad.get_calibrated_S())
        specData.append(specTriad.get_calibrated_J())
        specData.append(specTriad.get_calibrated_T())
        specData.append(specTriad.get_calibrated_U())
        specData.append(specTriad.get_calibrated_V())
        specData.append(specTriad.get_calibrated_W())
        specData.append(specTriad.get_calibrated_K())
        specData.append(specTriad.get_calibrated_L())
        
        
        '''debug'''
        print("Probe Temp:")
        print(tempList)
        print("Ambient data (Temp, Temp, Pressure, Humidity):")
        print(ambientData)
        print("Soil moisture:")
        print(soilMoist)
        print("Luminosity:")
        print(fullLux)
        #print(fullLux, irLux, totalLux)
        print("Spectral Data (ABCDEFGHRISJTUVWKL):")
        print(specData) 
        
        #take_image()
        time.sleep(1)

        '''
        ahtTest = str(tempHum.print())
        ahtTemp = tempHum.temperature()
        ahtHum = tempHum.humidity()
        tempList = []
        tempBus.convert_temp()
        time.sleep_ms(800)
        
        for i in temps:
            tempList.append(tempBus.read_temp(i))
        '''
        #print(tempList)
        #moist = analogMoist.read_u16() * 3.3 / 65536
        #print(moist)
        #print(ahtTest)
        
        
        
        #tempFile = open("image.jpeg",'r')
        #imageData = tempFile.read()
        #tempFile.close()
        
        
        testMsg = {"node": secretVars.nodeID,
                   "unitName": secretVars.unitName,
                   "UID": machine.unique_id(),
                   "soilTemp": tempList,
                   "soilMoist": soilMoist,
                   "ambTemp1": ambientData[0],
                   "ambTemp2": ambientData[1],
                   "ambPres": ambientData[2],
                   "ambHum": ambientData[3],
                   "dewPoint": ambientData[4], 
                   "lux": fullLux,
                   "spectral": specData,
                   "imageData": "pqmq1fqhVG7gaNMpWMQx8A==" #base64 data goes here
                   }
                 
        print(json.dumps(testMsg).encode())
        client.publish(secretVars.telemTopic, json.dumps(testMsg).encode())
        
        #collect garbage and close files
        print("meaningless change for update test, take 78")
        time.sleep(5)

main()
 
