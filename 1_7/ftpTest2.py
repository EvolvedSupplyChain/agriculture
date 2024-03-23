import time
from ftplib import FTP
from camera import *
import network
from umqttsimple import MQTTClient
import secretVars
import json
import machine
from ftpupload import upload
import ubinascii
import gc

'''wifi connection:'''
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(secretVars.ssid, secretVars.wifiPassword)

while station.isconnected() == False:
    pass
print(station.ifconfig())

'''MQTT:'''

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'notification' and msg == b'received':
    print('ESP received hello message')
  else:
    print('message recieved: ' + msg)

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(' camTest', secretVars.brokerAddress, keepalive=60)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(secretVars.ccTopic)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (secretVars.brokerAddress, secretVars.ccTopic))
  return client

client = connect_and_subscribe()

ftpClient = FTP()
ftpClient.connect('192.168.8.200')
ftpClient.login('Andy','2075012')

while True:
    take_image()
    time.sleep(5)
    print(gc.mem_free())
    gc.collect()
    print(gc.mem_free())
    theFile = open('image.jpeg','rb')
    picture = bytearray(theFile.read())
    #convert = ubinascii.b2a_base64(theFile.read())
    '''
    tempFile = open('image.txt','w')
    tempFile.write(convert)
    tempFile.close()
    '''
    theFile.close()
    #gc.collect()
    #print(upload(ftpClient, 'image.txt'))
    #print(upload(ftpClient, 'image.jpeg'))
    #tempFile = open("image.jpeg",'rb')
    #ftpClient.storbinary('STOR', tempFile)
    #time.sleep(10)
    #tempData = tempFile.read()
    #transData = bytearray(tempData)
    #tempFile.close()
    testMsg = {"node": 'camTest',
               "uniqueID": machine.unique_id(),
               "imageData": picture.decode()
              }
    
    #testMsg = json.dumps(testMsg).encode()
    #print(testMsg)
    #print(json.dumps(testMsg).encode())
    client.publish(secretVars.telemTopic, json.dumps(testMsg).encode())
    #client.publish(secretVars.telemTopic, json.stringify(testMsg))
    #theFile.close()
    time.sleep(5)
    gc.collect()