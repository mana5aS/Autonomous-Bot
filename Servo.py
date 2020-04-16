from gpiozero import Servo
from time import sleep
 
myGPIO=2
 
myCorrection=0.45
maxPW=(2.0+myCorrection)/1000
minPW=(1.0-myCorrection)/1000
 
servo = Servo(myGPIO,min_pulse_width=minPW,max_pulse_width=maxPW)
 
while True:
    servo.mid()
    print("mid")
    sleep(2)
    servo.min()
    print("min")
    sleep(2)
    servo.mid()
    print("mid")
    sleep(2)
    servo.max()
    print("max")
    sleep(2)