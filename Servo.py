#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
servoPIN = 2
GPIO.setup(servoPIN,GPIO.OUT)
pwm = GPIO.PWM(servoPIN,50)
pwm.start(0)

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(servoPIN, GPIO.HIGH)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servoPIN, GPIO.LOW)
    pwm.ChangeDutyCycle(0)

SetAngle(90)

if __name__ == '__main__':
   
    while True:
        pwm.ChangeDutyCycle(7.5) #Neutral
        time.sleep(1)
        pwm.ChangeDutyCycle(12.5) #180
        time.sleep(1)
        pwm.ChangeDutyCycle(2.5) #0
        time.sleep(1)        
