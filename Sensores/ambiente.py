import Adafruit_DHT
import threading
from time import sleep


class TemperaturaAmbiente(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.corriendo = True
        self.temperturaAmbiente = None
        self.humedadAmbiente = None
        self.sensor = Adafruit_DHT.AM2302
        self.pin = 23

    def run(self):
        sleep(5)
        try:
            while self.corriendo:
                humedad, temperatura = Adafruit_DHT.read_retry(self.sensor, self.pin)
                if humedad is not None and temperatura is not None:
                    self.humedadAmbiente = humedad
                    self.temperturaAmbiente = temperatura
        except:
            pass

    def getTemperaturaAmbiente(self):
        return self.temperturaAmbiente

    def getHumedadAmbiente(self):
        return self.humedadAmbiente

    def setCorriendo(self, bool):
        self.corriendo = bool

if __name__ == '__main__':

    temperaturaambiente = TemperaturaAmbiente()
    temperaturaambiente.start()

    while True:
        sleep(10)
        print('La humedad en este momento es {}'.format(temperaturaambiente.humedadAmbiente))
        print('La temperatura en este momento es {}'.format(temperaturaambiente.temperturaAmbiente))
