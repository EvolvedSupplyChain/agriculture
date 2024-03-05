from machine import Pin, ADC
import time

datapin = ADC(Pin(26, Pin.IN, Pin.PULL_DOWN))
powerpin = Pin(27, Pin.OUT)
powerpin.value(1)

def convert(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


while True:
    data = datapin.read_u16()
    time.sleep(2)
    print(data)
    data = data *3.2 / 65535 
    print(data)
    scaled = convert(data,0.0095,0.15,0,100)
    print(scaled)
    time.sleep(2)