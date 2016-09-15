import RPi.GPIO as GPIO
import control.pid as pid
import threading

class Control:

    def __init__(self, P = -60, I = -0.02 , D = 0, frecuencia = 500, ciclo = 100, salida = 12):
        threading.Thread.__init__(self)

        self.corriendo = True

        # Inicio del PID con las constantes
        # y ajuste de su setpoint
        self.pid = pid.PID(P, I, D)
        self.pid.set_point(6)

        # Revisar si ya se establecio
        # enumeracion en la Pi
        if GPIO.setmode() is None or GPIO.setmode() is GPIO.BOARD:
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
        try:
            temperatura = sensorTemperatura.getTemperaturaAmbiente()
            Ciclo = (self.pid.update(temperatura) / 24) * 100
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
