import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BCM)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]

bits = len(dac)
levels = 2**bits
comp = 14
troyka = 13

GPIO.setup(leds, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)

#функция перевода в двоичную
def decimal2binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

#функция АЦП
def adc():
    value_res = 0 
    temp_value = 0
    for i in range(8):
        pow2 = 2 ** (8 - i - 1)
        temp_value = value_res + pow2
        signal = decimal2binary(temp_value)
        GPIO.output(dac, signal)
        time.sleep(0.01)
        compVal = GPIO.input(comp)
        if compVal == 0:
            value_res = value_res + pow2
    return value_res



try:
    time_start = time.time()
    count = 0
    data = []
    data1 = []
    time_list = []
    voltage = 0

    #Зарядка конденсатора
    print('Зарядка конденсатора')
    while voltage <= 250:
        voltage = adc()
        print(voltage)
        data1.append(voltage)
        data.append(voltage/256*3.3)
        time_list.append(time.time() - time_start)
        time.sleep(0)
        count+=1
        GPIO.output(leds, decimal2binary(voltage))

    GPIO.output(troyka, 0)

    #Разрядка конденсатора
    print('Разрядка конденсатора')
    while voltage >= 60:
        voltage = adc()
        print(voltage)
        data1.append(voltage)
        data.append(voltage/256*3.3)
        time_list.append(time.time() - time_start)
        time.sleep(0)
        count+=1
        GPIO.output(leds, decimal2binary(voltage))
    

    #Ищем полное время эксперимента
    time_end = time.time()
    time_total = time_end - time_start

    print('Графики')

    #Строим графики
    plt.plot(time_list, data)
    plt.xlabel("Время")
    plt.ylabel("Напряжение")
    plt.show()

    print('Запись в файл')

    #Запись в файл
    with open('data.txt', "w") as f:
        for i in data1:
            f.write(str(i) + '\n')

    with open('settings.txt', "w") as f:
        f.write('' + str(1/time_total*count) + '\n')
        f.write('0.0129')

    print('Завершение программы')

finally:
    GPIO.output(leds, 0)
    GPIO.output(dac, 0)
    GPIO.cleanup()
    count = 0