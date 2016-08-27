import pid as pid
import pwm as pwm
import Adafruit_DHT
from time import sleep
import os

sensor = Adafruit_DHT.AM2302
pin = 23

p = pid.PID(1,1,0.02, Integrator_max=100, Integrator_min=0)
p.setPoint(29.0)


pwm_control = pwm.PWM(1000,0)

while True:
    sleep(.5)
    os.system('clear')
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    x = (p.update(temperature))*-1
    print x
    pwm_control.setCycle(x)
