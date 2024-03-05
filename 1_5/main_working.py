import utime
import time
from machine import Pin, SPI, I2C
#import Arducam 
import bmp280
import aht10
import onewire
import ds18x20
import as7265x
import TSL2591
import network
#from umqttsimple import MQTTClient
import secretVars
import ubinascii
import json

'''wifi connection:'''
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(secretVars.ssid, secretVars.wifiPassword)

while station.isconnected() == False:
    pass
print(station.ifconfig())


'''MQTT:
def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(secretVars.clientID, secretVars.brokerAddress, keepalive=60)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(secretVars.ccTopic)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (secretVars.brokerAddress, secretVars.ccTopic))
  return client

'''


'''ambient temp, humidity, and pressure sensors:'''
ambientPower = Pin(22, Pin.OUT)
ambientPower.value(1)
ambientI2CBus = I2C(0,scl=Pin(1),sda=Pin(0))
time.sleep_ms(200)
tempHum = aht10.AHT10(ambientI2CBus)
tempPres = bmp280.BMP280(ambientI2CBus)
tempPres.use_case(bmp280.BMP280_CASE_INDOOR)

'''spectral and lux sensors:'''
lightPower = Pin(21, Pin.OUT)
lightPower.value(1)
spectralI2CBus = I2C(1,scl=Pin(7),sda=Pin(6))
time.sleep_ms(200)
specTriad = as7265x.AS7265X(spectralI2CBus)
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
moistureProbeData = Pin(4, Pin.IN)
moistureProbePower = Pin(5,Pin.OUT)
moistureProbePower.value(0)

'''Camera:'''
#imageSense = ArducamClass(OV5642)
    


def main():
    

    tempBus = ds18x20.DS18X20(onewire.OneWire(tempProbeData))
    temps = tempBus.scan()
    
    while True:
        tempList = []
        tempBus.convert_temp()
        time.sleep_ms(800)
        for i in temps:
            tempList.append(tempBus.read_temp(i))
        
        #ambientData = [0,tempPres.temperature,tempPres.pressure,0]
        
        ambientData = [tempHum.temperature(),tempPres.temperature,tempPres.pressure,tempHum.humidity()]
        
        
        moistureProbePower.value(1)
        time.sleep_ms(300)
        soilMoist = moistureProbeData.value()
        time.sleep_ms(300)
        moistureProbePower.value(0)
        
        
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
        print(tempList)
        print(ambientData)
        print(soilMoist)
        print(fullLux)
        #print(fullLux, irLux, totalLux)
        print(specData) 
        
        
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
        



main()
