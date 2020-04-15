"""The Bot moves Forward, Back, Right and Left"""



#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#Motors
#MotorA
in1 = 9
in2 = 10
enA = 11

#MotorB
in3 = 22
in4 = 27
enB = 17

#MotorC
in5 = 24
in6 = 23
enC = 25

#MotorD
in7 = 18
in8 = 15
enD = 14

#Motors
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)
GPIO.setup(in5,GPIO.OUT)
GPIO.setup(in6,GPIO.OUT)
GPIO.setup(enC,GPIO.OUT)
GPIO.setup(in7,GPIO.OUT)
GPIO.setup(in8,GPIO.OUT)
GPIO.setup(enD,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
GPIO.output(in5,GPIO.LOW)
GPIO.output(in6,GPIO.LOW)
GPIO.output(in7,GPIO.LOW)
GPIO.output(in8,GPIO.LOW)

pA=GPIO.PWM(enA,100)
pB=GPIO.PWM(enB,100)
pC=GPIO.PWM(enC,100)
pD=GPIO.PWM(enD,100)

pA.start(100)
pB.start(100)
pC.start(100)
pD.start(100)


def goForward():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(enA,GPIO.HIGH)

    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(enB,GPIO.HIGH)

    GPIO.output(in5,GPIO.HIGH)
    GPIO.output(in6,GPIO.LOW)
    GPIO.output(enC,GPIO.HIGH)

    GPIO.output(in7,GPIO.HIGH)
    GPIO.output(in8,GPIO.LOW)
    GPIO.output(enD,GPIO.HIGH)


def goBack():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(enA,GPIO.HIGH)

    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    GPIO.output(enB,GPIO.HIGH)

    GPIO.output(in5,GPIO.LOW)
    GPIO.output(in6,GPIO.HIGH)
    GPIO.output(enC,GPIO.HIGH)

    GPIO.output(in7,GPIO.LOW)
    GPIO.output(in8,GPIO.HIGH)
    GPIO.output(enD,GPIO.HIGH)

def goLeft():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(enA,GPIO.HIGH)

    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(enB,GPIO.HIGH)

    GPIO.output(in5,GPIO.LOW)
    GPIO.output(in6,GPIO.LOW)
    GPIO.output(enC,GPIO.HIGH)

    GPIO.output(in7,GPIO.HIGH)
    GPIO.output(in8,GPIO.LOW)
    GPIO.output(enD,GPIO.HIGH)

def goRight():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(enA,GPIO.HIGH)

    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(enB,GPIO.HIGH)

    GPIO.output(in5,GPIO.HIGH)
    GPIO.output(in6,GPIO.LOW)
    GPIO.output(enC,GPIO.HIGH)

    GPIO.output(in7,GPIO.LOW)
    GPIO.output(in8,GPIO.LOW)
    GPIO.output(enD,GPIO.HIGH)



def stop():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(enA,GPIO.HIGH)

    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(enB,GPIO.HIGH)

    GPIO.output(in5,GPIO.LOW)
    GPIO.output(in6,GPIO.LOW)
    GPIO.output(enC,GPIO.HIGH)

    GPIO.output(in7,GPIO.LOW)
    GPIO.output(in8,GPIO.LOW)
    GPIO.output(enD,GPIO.HIGH)


if __name__ == '__main__':
   
    while True:
        goForward()
        time.sleep(3)
        goBack()
        time.sleep(3)
        goLeft()
        time.sleep(1)
        stop()
        time.sleep(1)
        goRight()
        time.sleep(1)
        stop() 
        time.sleep(1)
        goRight()
        time.sleep(1)
        stop()
        time.sleep(1)
        goLeft()
        time.sleep(1)
        stop() 
        time.sleep(3)
