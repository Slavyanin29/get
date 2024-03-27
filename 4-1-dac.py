import RPi.GPIO as GPIO

GPIO.setwarnings(False)

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

def decimalToBinary(val):
    if val < 0:
        return 'Not positive'
    else:
        return [int(element) for element in bin(val)[2:].zfill(8)]

try:
    while True:
        num = input("Type a number from 0 to 255:")
        try:
            num = int(num)
            if 0 <= num <= 255:
                GPIO.output(dac, decimalToBinary(num))
                voltage = float(num) / 256.0 * 3.3
                print(f"-->  Output voltage is about {voltage:.4} volt")
            else:
                if num < 0:
                    print("!!!  Number has to be >= 0! Try again...")
                elif num > 255:
                    print("!!!  Number has to be <= 255! Try again...")
        except Exception:
            if num == "q": break
            print("!!!  It must be a integer, not string or ! Try again...")

finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    print("EOP")