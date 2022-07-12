#Semi-automated dialysis code. Requires Python 3.10 or later

import RPi.GPIO as GPIO
import time
#pin assignments, uses GPIO numbers NOT the pin number
floatsensor = 4 #pin for float sensor
relayfill = 5 #pin for relay controlling the fill valve
relaydrain = 6 #pin for relay controlling the drain valve

#internal variables, those with comments are ones you might want to change
fullstate = 0
#auto = false
#fill = false
#full = false
#drain = false
#didit = false
filltimer = 0
draintimer = 0
stopfill = 5 #how long (in seconds) will the fill last
stopdrain = 5 #how long (in seconds) will the drain last
t = 0
cycleind = 0
cyclenum = 10 #how man dialysis cycles in the automatic setting (default 10)
cycletime = 7200 #how long each dialysis cycle lasts in modes 1 and initial cycle in mode 2 (default 7200)
dialysismode = 0
scalefactor = 0.2 #scale factor for increasing leng
cycleprogram = [7200, 14400, 14400, 14400, 14400, 28800, 28800] # cycle times (in seconds) for mode 3, default is 2hr, 4hr, 4hr, 4hr, 4hr, 8hr, 8hr
meastau = 100 #how many measurements to use to calculate tau
tau = 0 #time constant to be calculated for conductivity-driven water change program
x = 3 #number of "tau" to pass per cycle 1 = 63% to equil, 2 = 86%, 3 = 95%, 4 = 98%
run = true
command = "nil"

#initiallizes pins for valve and switch control. close all valves to start
GPIO.setmode(GPIO.BCM) # Choose BCM to use GPIO numbers instead of pin numbers
GPIO.setup(relayfill, GPIO.OUT)
GPIO.setup(relaydrain, GPIO.OUT)
GPIO.setup(floatsensor, GPIO.IN)
GPIO.output(relayfill, GPIO.LOW)
GPIO.output(relaydrain, GPIO.LOW)
fullstate = GPIO.input(floatsensor)

def filltank(): #fills the tank, checks floatswitch and timer every second, stops when either one engages first
	fullstate = GPIO.input(floatsensor)	
	if fullstate == 0:
		GPIO.output(relayfill, GPIO.HIGH)
		print('Filling now.')
	else:
		print('Tank is full.')
		return()
	while filltimer < stopfill and fullstate == 0: #&& is and in python I think
		fullstate = GPIO.input(floatsensor)
		print(stopfill - filltimer)
		sleep(1)
		filltimer += 1 #instead of ++
	GPIO.output(relayfill, GPIO.LOW)
	filltimer = 0
	print('Tank is full.')
	return()
		
def draintank(): #drains the tank on a timer, no float switch is used
	GPIO.output(relayfill, GPIO.LOW)
	GPIO.output(relaydrain, GPIO.HIGH)
	print('Draining now.')
	while draintimer < stopdrain:
		print(stopdrain - draintimer)
		sleep(1)
		draintimer += 1 #++
	GPIO.output(relaydrain, GPIO.LOW)
	draintimer = 0
	print('Tank is empty.')
	return()

def dialyze():
	print('Choose dialysis mode. "0" = fixed time/cycle, "1" = increasing time/cycle, "2" = preset program, "3" = conductivity-mediated dialysis mode, type "back" to go back, type "exit" to exit the program')
	dialysismode = input()
	while dialysismode != 'exit':
		match dialysismode:
			case '0':
				while cycleind < cyclenum:
					filltank()
					while t < cycletime:
						t +=1 #++
						#measure conductivity and temp
						print('Conductivity is now XYZ')
						sleep(1)
					t = 0
					draintank()
					cycleind +=1 #++
				print('Dialysis complete')
				return()
			case '1':
				while cycleind < cyclenum:
					filltank()
					while t < (cycletime+(cycletime*cycleind*scalefactor)):
						t +=1 #++
						#measure conductivity and temp
						print('Conductivity is now XYZ')
						sleep(1)
					t = 0
					draintank()
					cycleind +=1 #++
				print('Dialysis complete')
				return()
			case '2':
				for i in cycleprogram:
					filltank()
					while t < cycleprogram[i]:
						t+=1 #++
						#measure conductivity and temp
						print('Conductivity is now XYZ')
						sleep(1)
					t = 0
					draintank()
				print('Dialysis complete')
				return()
			case '3':
				#loop
					#filltank()
					#take some number of measurements
					#calculate tau
					#remaining time = tau*x - time for measurements
					#while t < remaining time:
						#t++
						#measure conductivity and temp
						#print('Conductivity is now XYZ')
						#sleep(1)
					#t = 0
					#draintank()
				print('This has not been impletented yet.')
				return()
			case 'back':
				return()
			case 'exit':
				command = 'exit'
				return()
			case _:
				print('Command not recognized.')

print('To start automatic dialysis type "start", to manually fill type "fill", to manually drain type "drain", to manually stop all filling and draining type "stop", to exit program type "exit"')

while command != 'exit':
	command = str.lower(input())
	match command.lower():
		case 'fill':
			filltank()
		case 'drain':
			draintank()
		case 'start':
			dialyze()
		case 'exit':
			print('Exiting')
		case _:
			print('Command not recognized.')

# while run: #main loop, really sloppy list of conditionals, only use for debugging

	# if fullstate == 1: #checks to see if the floatswitch is closed, if so then stops filling
		# GPIO.output(relayfill, GPIO.LOW)
		# full = true
		# fill = false
		# filltimer = 0
		# print('Tank is full.')
	
	# if fullstate != 1:
		# full = false
		
	# if command == "start":
		# auto = true
		# print('Starting automatic dialysis cycle.')
		# command = "fill"
	
	# if command == "fill" && fullstate != 1:
		# didit = true
		# fill = true
		# GPIO.output(relayfill, GPIO.HIGH)
		# print('Filling Now.')
	
	# if command == "drain":
		# didit = true
		# drain = true
		# GPIO.output(relaydrain, GPIO.HIGH)
		# print('Draining Now.')
		
	# if command == "stop":
		# didit = true
		# fill = false
		# drain = false
		# filltimer = 0
		# draintimer = 0
		# GPIO.output(relayfill, GPIO.LOW)
		# GPIO.output(relaydrain, GPIO.LOW)
		# print('Stopping.')
		
	# if command == "exit":
		# quit()
	
	# if fill == true:
		# sleep(1)
		# filltimer++
	
	# if drain == true:
		# sleep(1)
		# draintimer++
		
	# if filltimer >= stopfill:
		# GPIO.output(relayfill, GPIO.LOW)
		# full = true
		# fill = false
		# filltimer = 0
		# print('Tank is full.')
		
	# if draintimer >= stopdrain:
		# GPIO.output(relaydrain, GPIO.LOW)
		# drain = false
		# draintimer = 0
		# print('Tank is empty')
		
	# if auto == true && full == true && fill != true && !drain != true:
		# while t <= cycletime
			# t++
			# #measure temp and humidity
			# print('Conductivity is now XYZ')
			# sleep(1)
		# command = "drain"
		# cycleind++
		
	# if cycleind >= cyclenum:
		# print('Dialysis is done.')
		# quit()
	
	# if didit == true:
		# didit = false
		# command = "nil"
	
	# else:
		# print('Something went wrong.')
		# run = false