import threading
import Adafruit_GPIO.I2C as I2C
from time import sleep

class TemperaturaOrgano(threading.Thread):
    """
    Organ temperature sensor
    Class to read the sensor and output its
    temperature to be seen on screen
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.ADDRESS_DEVICE = 0x5A
        self.ADDRESS_OBJECT1 = 0x07
        self.sensor = I2C.Device(self.ADDRESS_DEVICE, 1)
        self.corriendo = True
        self.temperturaOrgano = None

    def run(self):
        sleep(5)
        try:
            while self.corriendo:
                ByteA = self.sensor.readS16(self.ADDRESS_OBJECT1)
                temperatura = (0.02*ByteA)-273.15
                if temperatura is not None:
                    self.temperturaOrgano = temperatura
      
        except:
            pass

    def getTemperaturaOrgano(self):
        return self.temperturaOrgano


    def setCorriendo(self, bool):
        self.corriendo = bool

if __name__ == '__main__':

    temperaturaorgano = TemperaturaOrgano()
    temperaturaorgano.start()

    while True:
        sleep(5)
        print('La temperatura del organo es: {}'.format(temperaturaorgano.temperturaOrgano))

