
#ADDRESS_DEVICE = 0x5A
#ADDRESS_OBJECT = 0x07
#-NO-I2C.require_repeated_start()
#sensor = I2C.Device(ADDRESS_DEVICE, 1)
#print(sensor)

#ByteA = sensor.readU16(ADDRESS_OBJECT)

#print(ByteA/50-273.15)

import threading
import Adafruit_GPIO.I2C as I2C
from time import sleep

class TemperaturaOrgano(threading.Thread):

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

