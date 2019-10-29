import motor_functions as mf
import time

motor = mf.Motor(4)

motor.clockwise(4)
time.sleep(2)
motor.counter_clockwise(3)
motor.close()