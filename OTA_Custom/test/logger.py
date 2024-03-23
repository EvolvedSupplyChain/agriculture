import machine
import time

#def main():
print("Attempt number 1")
led = machine.Pin('LED', machine.Pin.OUT)
    
while True:
    led.toggle()
    print("5555")
    time.sleep(1)
