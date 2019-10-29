import RPi.GPIO as gp
import time


class VexMotor:
    def __init__(self, pin):
        self.on = False
        self.onPWM = 22
        self.offPWM = 0
        
        gp.setmode(gp.BCM)
        self.motor = pin
        gp.setup(self.motor, gp.OUT)
        
        self.p = gp.PWM(self.motor, 100)
        self.p.start(0)

    def toggle(self):
        self.on = not self.on
                    
    def test(self):
        for i in range(1, 51):
            self.p.ChangeDutyCycle(i)
            print(i)
            time.sleep(0.5)
    
    def run(self):
        if self.on:
            self.p.ChangeDutyCycle(self.onPWM)
        else:
            self.p.ChangeDutyCycle(self.offPWM)

    def close(self):
        gp.cleanup()
        print('closed gpio')


class MiniCIMMotor:
    def __init__(self, pin, inverse=False):
        self.inverse = inverse
        self.basecc = 14
        self.baseccw = 15
            
        self.offPWM = 0
            
        self.cc = 0
        self.ccw = 0  
        
        gp.setmode(gp.BCM)
        self.motor = pin
        gp.setup(self.motor, gp.OUT)
        
        self.p = gp.PWM(self.motor, 100)
        self.p.start(0)

    def forward(self, power):
        if not self.inverse:
            if power >= 8:
                power = 8
                self.ccw = self.baseccw - power 
            elif power == -1:
                self.ccw = self.offPWM
            else:
                self.ccw = self.baseccw - power
        else:
            if power >= 8:
                power = 8
                self.cc = self.basecc + power 
            elif power == -1:
                self.cc = self.offPWM
            else:
                self.cc = self.basecc + power
        
    def backward(self, power):
        if not self.inverse:
            if power >= 8:
                power = 8
                self.cc = self.basecc + power 
            elif power == -1:
                self.cc = self.offPWM
            else:
                self.cc = self.basecc + power
        else:
            if power >= 8:
                power = 8
                self.ccw = self.baseccw - power 
            elif power == -1:
                self.ccw = self.offPWM
            else:
                self.ccw = self.baseccw - power
            
    def off(self):
        self.ccw = self.offPWM
        self.cc = self.offPWM
        
    def run(self):
        if self.cc > self.ccw:
            self.p.ChangeDutyCycle(self.cc)
        elif self.cc < self.ccw:
            self.p.ChangeDutyCycle(self.ccw)
        else:
            self.p.ChangeDutyCycle(self.offPWM)

    def close(self):
        gp.cleanup()
        print('closed gpio')

def main():
    m = Motor(4)
    while True:
        try:
            for i in range(9):
                m.counter_clockwise(i)
                m.run()
                time.sleep(0.4)
        
        except KeyboardInterrupt:
            m.close()
    """
    m.clockwise(5)
    time.sleep(2)
    
    
    m.counter_clockwise(4)
    m.close()
    """

if __name__ == '__main__':
    main()
