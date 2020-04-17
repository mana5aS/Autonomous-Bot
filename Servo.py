#!/usr/bin/python

import pigpio
import time

pi = pigpio.pi()
pi.set_mode(2, pigpio.OUTPUT)
pi.get_mode(2)

while True : 

   pi.set_servo_pulsewidth(2, 1500)  #mid
   pi.get_servo_pulsewidth(2)
   time.sleep(2)

   pi.set_servo_pulsewidth(2, 500)  #right
   pi.get_servo_pulsewidth(2)
   time.sleep(2)

   pi.set_servo_pulsewidth(2, 1500)  #mid
   pi.get_servo_pulsewidth(2)
   time.sleep(2)
   
   pi.set_servo_pulsewidth(2, 2500) #left
   pi.get_servo_pulsewidth(2)
   time.sleep(2)

pi.stop()