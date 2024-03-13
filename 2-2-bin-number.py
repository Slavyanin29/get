import RPi.GPIO as GPIO
import time

def bin_translator(num):
    number = [0, 0, 0, 0, 0, 0, 0, 0]
    d_num = num % 256
    bin_num = bin(d_num)
    i = -1
    while bin_num[i] != 'b':
        number[i] = int(bin_num[i])
        i -= 1
    print("{} --> {}".format(num, number))
    GPIO.output(dac, number)
    return 0                                                                                      

dac = [8, 11, 7, 1, 0, 5, 12, 6]
nums = [0, 5, 32, 64, 127, 255, 256]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

for i in nums:
    bin_translator(i)
    time.sleep(15)

GPIO.output(dac, 0)
GPIO.cleanup()