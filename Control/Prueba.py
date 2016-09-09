import pid as pid
import pwm as pwm
import Adafruit_DHT
import RPi.GPIO as GPIO
from time import sleep
import os

sensor = Adafruit_DHT.AM2302
pin = 23

p = pid.PID(-60, -0.02, 0, Integrator_max=100, Integrator_min=-100)
p.setPoint(8)

GPIO.setmode(GPIO.BCM)

GPIO.setup(16, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

GPIO.output(16, GPIO.HIGH)
GPIO.output(21, GPIO.LOW)

fan = pwm.PWM(500, 0, 0, 12)
fan.startPWM()

try:
    while True:
        sleep(.5)
        os.system('clear')
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        Ciclo = (p.update(temperature)/24)*100
        try :
            fan.setCycle(Ciclo)
        except :
            print('No se pudo leer el sensor')
        print(str(temperature))
        print(str(Ciclo))

except KeyboardInterrupt:
  pass
