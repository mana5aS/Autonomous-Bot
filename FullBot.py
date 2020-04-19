#Libraries
import RPi.GPIO as GPIO
import time
import pigpio
import numpy as np
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#Ultrasonic
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 3
ECHO = 4
maxTime = 0.04
minDistance = 10

#Servo
pi = pigpio.pi()
pi.set_mode(2, pigpio.OUTPUT)
pi.get_mode(2)

#Motors
# #MotorA
# in1 = 9
# in2 = 10
# enA = 11

# #MotorB
# in3 = 22
# in4 = 27
# enB = 17

#Motor A and C
in1 = 24
in2 = 23
enA = 25

#Motor B and D
in3 = 18
in4 = 15
enB = 14

#Motors
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)


GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)


pA=GPIO.PWM(enA,100)
pB=GPIO.PWM(enB,100)

pA.start(100)
pB.start(100)

G_length = 80  #full grid length
gridLength = G_length - minDistance - 10 - 40#effective grid length 10 is leeway
traversedDistance = 0

row, col = (20,20)
maze = [[-1 for i in range(col)] for j in range(row)] 
direction = 0 #  0-forward(+i) 1-right(+j) 2-back(-i) 3-left(-j) 
i = 0
j = 0
maze[0][0] = 2 #2 is home

rightTurnTime = 0.8
leftTurnTime = 0.8



def goForward():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(enA,GPIO.HIGH)

    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(enB,GPIO.HIGH)
    

def goBack():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(enA,GPIO.HIGH)

    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    GPIO.output(enB,GPIO.HIGH)

    
def goLeft():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(enA,GPIO.HIGH)

    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(enB,GPIO.HIGH)


def pivotLeft():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(enA,GPIO.HIGH)

    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(enB,GPIO.HIGH)  


def pivotRight():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(enA,GPIO.HIGH) 

    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    GPIO.output(enB,GPIO.HIGH)

    
def goRight():
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(enA,GPIO.HIGH)

    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(enB,GPIO.HIGH)

    
def stop():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(enA,GPIO.HIGH)

    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(enB,GPIO.HIGH)

    
def getDistance():
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    GPIO.output(TRIG,False)

    time.sleep(0.01)

    GPIO.output(TRIG,True)

    time.sleep(0.00001)

    GPIO.output(TRIG,False)

    pulse_start = time.time()
    timeout = pulse_start + maxTime
    while GPIO.input(ECHO) == 0 and pulse_start < timeout:
        pulse_start = time.time()

    pulse_end = time.time()
    timeout = pulse_end + maxTime
    while GPIO.input(ECHO) == 1 and pulse_end < timeout:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17000
    distance = round(distance, 2)

    return distance


if __name__ == '__main__':

    pi.set_servo_pulsewidth(2, 1500)  #mid
    pi.get_servo_pulsewidth(2)
    time.sleep(2)
   
    while True:
        distance = getDistance()
        #print("distance = ",distance)
        if( distance <= minDistance):
            stop()
            maze[i][j] = 0             #mark grid as occupied
            print("\t\t",i," ",j)
            np.savetxt('maze.txt', maze, fmt='%s')
            traversedDistance = 0      #reset
            print("stop")
            goBack()
            time.sleep(0.5)
            stop()
            time.sleep(0.5)
            maxDistLeft = 0
            maxDistRight = 0

            time.sleep(0.5)           

            pi.set_servo_pulsewidth(2, 500)  #right
            pi.get_servo_pulsewidth(2)
            time.sleep(2)

            maxDistRight = getDistance()
            #print("Right = ",maxDistRight)

            pi.set_servo_pulsewidth(2, 1500)  #mid
            pi.get_servo_pulsewidth(2)
            time.sleep(2)
   
            pi.set_servo_pulsewidth(2, 2500) #left
            pi.get_servo_pulsewidth(2)
            time.sleep(2)

            pi.set_servo_pulsewidth(2, 1500)  #mid
            pi.get_servo_pulsewidth(2)
            time.sleep(2)


            maxDistLeft = getDistance()
            #print("left = ",maxDistLeft)
            
            if (maxDistLeft <=20 and maxDistRight <= 20):
                goBack()
                time.sleep(0.5)


            elif(maxDistLeft <= maxDistRight):
                #goRight()
                pivotRight()                
                time.sleep(rightTurnTime)
                direction += 1

            else:
                #goLeft()
                pivotLeft()                
                time.sleep(leftTurnTime)
                direction -= 1
        
        else:
            goForward()
            traversedDistance += 1
            if traversedDistance > gridLength :  
                traversedDistance = 0              
                if (direction%4) == 0 :
                    j += 1
                elif (direction%4) == 1:
                    i += 1
                elif (direction%4) == 2:
                    j -= 1
                elif (direction%4) == 3:
                    i -= 1
                maze[i][j] = 1
                print("\t\t",i," ",j)
                np.savetxt('maze.txt', maze, fmt='%s')

            #print("moving Forward", traversedDistance)
            
