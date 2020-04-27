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

TRIG = 17   #3
ECHO = 27   #4
maxTime = 0.04
minDistance = 10

#Servo
pi = pigpio.pi()
pi.set_mode(2, pigpio.OUTPUT)
pi.get_mode(2)

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

def pivotLeft():
	GPIO.output(in1,GPIO.LOW)
	GPIO.output(in2,GPIO.HIGH)
	GPIO.output(enA,GPIO.HIGH)

	GPIO.output(in3,GPIO.HIGH)
	GPIO.output(in4,GPIO.LOW)
	GPIO.output(enB,GPIO.HIGH) 

	time.sleep(leftTurnTime) 

def pivotRight():
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(enA,GPIO.HIGH) 

	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.HIGH)
	GPIO.output(enB,GPIO.HIGH)

	time.sleep(rightTurnTime)

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
	return  distance

def lookLeftAndRight():
	pi.set_servo_pulsewidth(2, 600)  #right
	pi.get_servo_pulsewidth(2)
	time.sleep(2)

	pi.set_servo_pulsewidth(2, 1500)  #mid
	pi.get_servo_pulsewidth(2)
	time.sleep(2)
		
	pi.set_servo_pulsewidth(2, 2300) #left
	pi.get_servo_pulsewidth(2)
	time.sleep(2)

	pi.set_servo_pulsewidth(2, 1500)  #mid
	pi.get_servo_pulsewidth(2)

minDistance = 10
forwardRange = 80
rightTurnTime = 0.78
leftTurnTime = 0.8

if __name__ == '__main__':

	while(True):
		stop()
		count = 0
		direction = input("enter direction: ").upper()

		if direction == "W":
			for _ in range(forwardRange):				
				if getDistance() < 10:
					count += 1
				if count == 3:
					stop()
					print("Obstruction Detected")
				goForward()
		elif direction == "A":
		 	pivotLeft()
		elif direction == "D":
			pivotRight()
		elif direction == "S":
			lookLeftAndRight()
			