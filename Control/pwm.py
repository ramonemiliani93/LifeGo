import RPi.GPIO as GPIO 

#Set mode for GPIO

class PWM:
    """
    Controlador PWM
    """

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12, GPIO.OUT)
    fan = GPIO.PWM(12,1000)
    fan.start(0)
    
    def __init__(self, frequency, cycle) :

        self.frequency = frequency
        self.cycle = cycle
        
    def setFrequency(self,new_frequency):
        self.frequency = new_frequency
        self.PWM_control = GPIO.PWM(self.output,self.frequency)

    def setCycle(self, new_cycle):
        if (new_cycle<0):
            self.cycle=0
        elif (new_cycle>100):
            self.cycle=100
        else:
            self.cycle = new_cycle
        #self.PWM_control.ChangeDutyCycle(self.cycle)
        

