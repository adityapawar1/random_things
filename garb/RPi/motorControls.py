import RPi.GPIO as gp
import time

class Motor:
    def __init__(self, pin):
        self.cwPWM = 6
        self.ccPWM = 24
        
        gp.setmode(gp.BCM)
        self.motor = pin
        gp.setup(self.motor, gp.OUT)
        
        self.p = gp.PWM(self.motor, 100)
        self.p.start(0)

    def counter_clockwise(self, mTime):
        self.p.ChangeDutyCycle(self.ccPWM)
        time.sleep(mTime)

    def clockwise(self, mTime):
        self.p.ChangeDutyCycle(self.cwPWM)
        time.sleep(mTime)

    def close(self):
        gp.cleanup()
        print('closed gpio')

def main():
    m = Motor(4)
    m.clockwise(5)
    time.sleep(2)
    m.counter_clockwise(4)
    m.close()

if __name__ == '__main__':
    main()
