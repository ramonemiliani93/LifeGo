import os, sys
sys.path.insert(0, '/home/pi/Documents/LifeGo/LifeGo/Sensores')
import RPi.GPIO as GPIO
import threading
import pid
import ambiente
from time import sleep

class Control:

    def __init__(self, P = -35, I = -0.02 , D = 0, frecuencia = 1000, ciclo = 100, salida = 12):
        self.corriendo = True

        # Inicio del PID con las constantes
        # y ajuste de su setpoint
        self.pid = pid.PID(P, I, D)
        self.pid.setPoint(15)

        # Revisar si ya se establecio
        # enumeracion en la Pi
        if GPIO.getmode() is None or GPIO.getmode() is GPIO.BOARD:
            GPIO.setmode(GPIO.BCM)

        # Ajustar pines de salida para el
        # puente h
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(21, GPIO.OUT)

        GPIO.output(16, GPIO.HIGH)
        GPIO.output(21, GPIO.LOW)

        # Ajustar salida al pin establecido
        GPIO.setup(salida, GPIO.OUT)

        # Inicar PWM
        self.PWM = GPIO.PWM(salida, frecuencia)
        self.PWM.start(ciclo)

    def actualizar(self, sensorTemperatura):
        while self.corriendo:
            sleep(5)
            print('Actualizando PID...')
            try:
                temperatura = sensorTemperatura.getTemperaturaAmbiente()
                print(('Temperatura: {}'.format(temperatura)))
                Ciclo = (self.pid.update(temperatura) / 24) * 100
                print(('Ciclo: {}'.format(Ciclo)))
                if Ciclo is not None:
                    if (Ciclo < 0):
                        Ciclo = 0
                    elif (Ciclo > 100):
                        Ciclo = 100
                    self.PWM.ChangeDutyCycle(Ciclo)
            except:
                print('No se pudo leer el hilo correspondiente al sensor')

    def setPoint(self, temperatura):
        self.pid.set_point(temperatura)

if __name__ == '__main__':
    print('Inicio Control')
    control = Control()
    print('Hilo temperatura')
    temperaturaambiente = ambiente.TemperaturaAmbiente()
    temperaturaambiente.start()
    print('Inicio Hilo Actualizar PID')
    threading.Thread(target=control.actualizar,args=(temperaturaambiente,)).start()
