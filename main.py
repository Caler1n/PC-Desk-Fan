#Desk Fan
#One Button Controls left to right movement
#Three buttons set max, medium, slow speeds

import RPi.GPIO as GPIO
import time

#Pin def
sideLED = 18
pwrLED = 22
sideToSide = 11
off  = 12
slow = 13
mid  = 15
fast = 16
fanCtrl = 32
servo = 33

#vars
offState = False
sideState = False
angle = 0
sideDir = -1
lastSide = time.time()

# Pins init
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pwrLED, GPIO.OUT)
GPIO.output(pwrLED, GPIO.LOW)
GPIO.setup(sideLED, GPIO.OUT)
GPIO.output(sideLED, GPIO.LOW)
GPIO.setup(sideToSide, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set button's mode as input, and pull up
GPIO.setup(off, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(slow, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(mid, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(fast, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#PWM Fan Ctrl Init
GPIO.setup(fanCtrl, GPIO.OUT)
fan = GPIO.PWM(fanCtrl,25000)
fan.start(0)

GPIO.setup(servo, GPIO.OUT)
mtr = GPIO.PWM(servo,50)
mtr.start(0)
 
try:
	while True:
			#Power Button Latching Code
			if GPIO.input(off) == GPIO.LOW:
				time.sleep(0.3)
				while (GPIO.input(off) == GPIO.LOW):
					pass
				offState = not offState
				GPIO.output(pwrLED, offState)  # turn led1 on
				if offState:
					print("Fan: ON")
					fan.ChangeDutyCycle(100)
				else:
					print("Fan: OFF")
					mtr.ChangeDutyCycle(0)
			if not offState:
				GPIO.output(sideLED, GPIO.LOW)    
            #Side to Side Movement Latching Code
			if offState:
				if GPIO.input(sideToSide) == GPIO.LOW:
					time.sleep(0.3)
					while (GPIO.input(sideToSide) == GPIO.LOW):
						pass
					sideState = not sideState
					GPIO.output(sideLED, sideState)  # turn led1 on
					if sideState:
						print("Moving: ON")
					else:
						print("Moving: OFF")
			
            #Fan Speed Button Logic
			if offState:
				if GPIO.input(slow) == GPIO.LOW:
					fan.ChangeDutyCycle(30)
					print("Fan Speed: Slow")
					time.sleep(0.3)
				elif offState and GPIO.input(mid) == GPIO.LOW:
					print("Fan Speed: Medium")
					fan.ChangeDutyCycle(60)
					time.sleep(0.3)
				elif offState and GPIO.input(fast) == GPIO.LOW:
					print("Fan Speed: Fast")
					fan.ChangeDutyCycle(100)
					time.sleep(0.3)
							
			if offState and sideState and (time.time() - lastSide) > 0.1:
				GPIO.output(sideLED, sideState)
				duty = 2.5 + 10 * angle / 180
				mtr.ChangeDutyCycle(duty)
				lastSide = time.time()
				
				angle += 1 * sideDir
				if angle >= 90:
					angle = 90
					sideDir = -1
				elif angle <= 0:
					angle = 0
					sideDir = 1
				elif not sideState:
					mtr.ChangeDutyCycle(0)

except KeyboardInterrupt:               #set up keyboard interrupt ctrl C
	fan.stop()
	mtr.stop()
	GPIO.output(pwrLED, GPIO.LOW)
	time.sleep(0.5)
	GPIO.cleanup()                          #cleanup all used GPIO pins
	print ("Ending program")                #print end of program to terminal
  
