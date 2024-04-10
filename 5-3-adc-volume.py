import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

led = [9, 10, 22, 27, 17, 4, 3, 2]
dac = [8, 11, 7, 1, 0, 5, 12, 6]
troika = 13
comp = 14

GPIO.setup(led, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troika, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(val):
        return [int(element) for element in bin(val)[2:].zfill(8)]

def adc():
    dac_val = [0 for i in range(8)]
    for i in range (8):
        dac_val[i] = 1
        GPIO.output(dac, dac_val)
        sleep(0.01)
        comp_val = GPIO.input(comp)
        if comp_val == 1:
            dac_val[i] = 0
    val = 0
    for i in range(8):
        val += dac_val[i] * (2 ** (7-i))
    return val

def Volume(val):
    volume = [0 for i in range(8)]
    step = 256 / 8
    for i in range(8):
        if val > step * i:
            volume[i] = 1
    return volume

try:
    while True:
        i = adc()
        volume_val = Volume(i)
        GPIO.output(led, volume_val)
        print(int(i/256*10))
finally:
    GPIO.output(led, 0)
    GPIO.output(dac, 0)
    GPIO.cleanup()
    print("EOP")