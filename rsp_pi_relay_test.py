#with RPi.GPIO (Python)
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) # Choose BCM to use GPIO numbers instead of pin numbers
GPIO.setup(17, GPIO.OUT) # GPIO17 = Pin 11
i = 10
for i in range(0,9):
	GPIO.output(17, GPIO.HIGH)
	time.sleep(1)
	GPIO.output(17, GPIO.LOW)
	time.sleep(1)

