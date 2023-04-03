import RPi.GPIO as GPIO
import time as t

GPIO.setmode(GPIO.BCM)
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
leds = [24, 25, 8, 7, 12, 16, 20, 21]
troyka = 17
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp,GPIO.IN)
GPIO.setup(leds, GPIO.OUT)

def perev(a):
    return[int(elem) for elem in bin(a)[2:].zfill(8)]

def adc():
    for a in range(256):
        signal = perev(a)
        GPIO.output(dac, signal)
        compvalue = GPIO.input(comp)
        time.sleep(0.005)
        if compvalue == 0:
            return a


def adc2():
    k = 0
    for i in range (7, -1, -1):
        k+=2**i
        GPIO.output(dac, perev(k))
        t.sleep(0.005)
        if GPIO.input(comp) == 0:
            k -=2**i
    return k

def toleds(k):
    return [1] * (k//32) +[0] * (8 - k //32)

try:
    while True:
        k = adc2()
        GPIO.output(leds, toleds(k))
finally:
    GPIO.output(dac,0)
    GPIO.cleanup()
