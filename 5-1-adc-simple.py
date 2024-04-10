import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
troika = 13
comp = 14

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troika, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(val):
        return [int(element) for element in bin(val)[2:].zfill(8)]

def adc():
    for i in range (256):
        dac_val = dec2bin(i)
        GPIO.output(dac, dac_val)
        comp_val = GPIO.input(comp)
        sleep(0.01)
        if comp_val:
            return i
    return 0

try:
    while True:
        i = adc()
        voltage = i * 3.3 / 256.0
        if i: print("{:.2f}V".format(voltage))
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    print("EOP")