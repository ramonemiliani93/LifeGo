import os, sys
sys.path.insert(0, '/home/pi/Documents/LifeGo/LifeGo/Sensores')
import RPi.GPIO as GPIO
import threading
import pid
import ambiente
import organo
from time import sleep
import datetime

class Control:

    def __init__(self, P = -35, I = -0.02 , D = 0, frecuencia = 1000, ciclo = 100, salida = 13):
        self.corriendo = True

        # Inicio del PID con las constantes
        # y ajuste de su setpoint
        self.pid = pid.PID(P, I, D)
        self.pid.setPoint(-500)

        # Revisar si ya se establecio
        # enumeracion en la Pi
        if GPIO.getmode() is None or GPIO.getmode() is GPIO.BOARD:
            GPIO.setmode(GPIO.BCM)

        # Ajustar pines de salida para el
        # puente h
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)

        GPIO.output(12, GPIO.HIGH)
        GPIO.output(16, GPIO.LOW)

        # Ajustar salida al pin establecido
        GPIO.setup(salida, GPIO.OUT)

        # Inicar PWM
        self.PWM = GPIO.PWM(salida, frecuencia)
        self.PWM.start(ciclo)

    def actualizar(self, sensorTemperatura, sensorOrgano):
        while self.corriendo:
            sleep(5)
            print('Actualizando PID...')
            try:
                organo = sensorOrgano.getTemperaturaOrgano()
                temperatura = sensorTemperatura.getTemperaturaAmbiente()
                humedad = sensorTemperatura.getHumedadAmbiente()
                print(('Temperatura Organo: {}'.format(organo)))
                print(('Temperatura Ambiente: {}'.format(temperatura)))
                print(('Humedad: {}'.format(humedad)))
                Ciclo = (self.pid.update(temperatura) / 24) * 100
                print(('Ciclo: {}'.format(Ciclo)))
                if Ciclo is not None:
                    if (Ciclo < 0):
                        Ciclo = 0
                    elif (Ciclo > 100):
                        Ciclo = 100
                    self.PWM.ChangeDutyCycle(Ciclo)
                ######################LOGGER#####################
                f=open('datos.txt','a')
                now = datetime.datetime.now()
                timestamp = now.strftime("%H:%M:%S")
                outstring = str(timestamp)+","+str(temperatura)+","+str(humedad)+","+str(organo)+"\n"
                f.write(outstring)
                f.close()
                #################################################
            except:
                print('No se pudo leer el hilo correspondiente al sensor')

    def setPoint(self, temperatura):
        self.pid.setPoint(temperatura)

if __name__ == '__main__':
    print('Inicio Control')
    control = Control()
    temperaturaorgano = organo.TemperaturaOrgano()
    print('Hilo temperatura organo')
    temperaturaambiente = ambiente.TemperaturaAmbiente()
    print('Hilo temperatura ambiente')
    temperaturaorgano.start()
    temperaturaambiente.start()
    print('Inicio Hilo Actualizar PID')
    threading.Thread(target=control.actualizar,args=(temperaturaambiente, temperaturaorgano,)).start()
