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

rightTurnTime = 0.78
leftTurnTime = 0.8

cell= "valid"


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

	time.sleep(leftTurnTime) 


def pivotRight():
	GPIO.output(in1,GPIO.HIGH)
	GPIO.output(in2,GPIO.LOW)
	GPIO.output(enA,GPIO.HIGH) 

	GPIO.output(in3,GPIO.LOW)
	GPIO.output(in4,GPIO.HIGH)
	GPIO.output(enB,GPIO.HIGH)

	time.sleep(rightTurnTime)

	
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
	return  distance


def getRightDistance():
	pi.set_servo_pulsewidth(2, 500)  #right
	pi.get_servo_pulsewidth(2)
	time.sleep(2)
	return(getDistance())


def getLeftDistance():
	pi.set_servo_pulsewidth(2, 2500) #left
	pi.get_servo_pulsewidth(2)
	time.sleep(2)
	return(getDistance())


def lookStraight():
	pi.set_servo_pulsewidth(2, 1500)  #mid
	pi.get_servo_pulsewidth(2)
	time.sleep(2)


def updateDirection(i, j, direction) :
	if (direction%4) == 0:
		j += 1		
	elif (direction%4) == 1:
		i += 1
	elif (direction%4) == 2:
		j -= 1
	elif (direction%4) == 3:
		i -= 1	
	return ([i, j])


def checkCell(i,j):
	if maze[i][j] == wall or maze[i][j] == 1 or maze[i][j] == 0: #maze[i][j] >= 0 :     #i in [0,i_max+1] or j in [0,j_max+] (can write this instead of wall)
		if (direction%4) == 0:
			j -= 1		
		elif (direction%4) == 1:
			i -= 1
		elif (direction%4) == 2:
			j += 1
		elif (direction%4) == 3:
			i += 1	
		return (["invalid",i,j])	
	else:
		return(["valid",i,j])

count = 0
minDistance = 10
cell ="valid"
traversedDistance = 0
gridLength = 50
i_max = 4
j_max = 4
row, col = (i_max+2,j_max+2)                                    #refer to mazecode and see the 
unoccupied = 2	                                                  #and see the output file maze.txt
maze = [[unoccupied for i in range(col)] for j in range(row)]   #to understance this part
wall = "*"
for i in range(i_max+2):                                        #Create maze
	maze[0][i] = wall
	maze[i_max+1][i] = wall
	maze[i][0] = wall
	maze[i][i_max+1] = wall 

direction = 0 #  0-forward(+j) 1-right(+i) 2-back(-j) 3-left(-i) 
i = 1
j = 1
flag =True

if __name__ == '__main__':

	lookStraight()
   
	while flag:

		distance = getDistance()
		print(traversedDistance,"i=",i,"j=",j,"  ","distance=",distance)		
		
		if distance <= minDistance or cell == "invalid" :						
			stop()			
			time.sleep(0.5)
			traversedDistance = -(0*minDistance)      #reset			
			if cell == "valid":
				maze[i][j] = 0                        #Obstruction
				print("00000000000000000000000000000000000000000000000000000000000")
				np.savetxt('maze.txt', maze, fmt='%s')
				

			Left_i, Left_j = updateDirection(i,j,direction-1)
			statusOfLeftCell,_,_ =  checkCell(Left_i,Left_j)
			Right_i, Right_j = updateDirection(i,j,direction+1)
			statusOfRightCell,_,_ = checkCell(Right_i,Right_j)

			if statusOfRightCell == "valid" and statusOfLeftCell == "valid" :				
				maxDistRight = getRightDistance()
				lookStraight()
				maxDistLeft = getLeftDistance()
				lookStraight()
				if maxDistLeft <= maxDistRight :
					pivotRight()
					direction += 1			
					if cell == "invalid" :
						i,j = updateDirection(i,j,direction)
				else :
					pivotLeft()
					direction =- 1	
					if cell == "invalid" :
						i,j = updateDirection(i,j,direction)				
			elif statusOfRightCell == "valid" :
				pivotRight()
				direction += 1
				if cell == "invalid" :
					i,j = updateDirection(i,j,direction)				
			elif statusOfLeftCell == "valid" :
				pivotLeft()
				direction -= 1
				if cell == "invalid" :
					i,j = updateDirection(i,j,direction)				
			else :
				print("no known path available",i,j,sep="\t")
				flag = False
			cell = "valid"                                #reset

		else :
			goForward()
			traversedDistance += 1				
			if traversedDistance > gridLength :	
				stop()			
				time.sleep(0.1)
				traversedDistance = 0
				#count += 1
				maze[i][j] = 1  #count                      #path
				np.savetxt('maze.txt', maze, fmt='%s')				
				print("old",i,j,count)
				i,j = updateDirection(i,j,direction)
				print("\tupdate",i,j,count)
				cell,i,j = checkCell(i,j)
				print("\t\taftercheck",cell,i,j,count)		