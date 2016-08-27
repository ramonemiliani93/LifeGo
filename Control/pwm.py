import RPi.GPIO as GPIO 

#Set mode for GPIO

class PWM:
    """
    Controlador PWM
    """
    
    def __init__(self, frequency, cycleStart, cycle, output) :

        self.frequency = frequency
        self.cycleStart = cycleStart
        self.cycle = cycle
        self.output = output

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(output, GPIO.OUT)

        self.PWM_control = GPIO.PWM(output,frequency)
        
    def setFrequency(self,new_frequency):
        self.frequency = new_frequency
        self.PWM_control.ChangeFrequency(new_frequency)

    def setCycle(self, new_cycle):
        if (new_cycle<0):
            self.cycle=0
        elif (new_cycle>100):
            self.cycle=100
        else:
            self.cycle = new_cycle
        self.PWM_control.ChangeDutyCycle(self.cycle)

    def startPWM(self):
        self.PWM_control.start(self.cycleStart)
