# ---------------------------------- make2explore.com-------------------------------------------------------------------------#
# Project           - Face Recognition based Door/Gate Security System 
# Created By        - info@make2explore.com
# Version - 1.0
# Last Modified     - 24/02/2022 15:00:00 @admin
# Software          - Python, Thonny IDE, Standard Python Libraries, OpenCV, Keras, TensorFlow etc.
# Hardware          - Raspberry Pi 4 model B, Logitech c270 webcam, i2c LCD, EM-18 RFID Reader, Level Converter, SG-90 Servo
# Sensors Used      - EM-18 RFID Reader, Logitech c270 webcam
# Source Repo       - https://github.com/make2explore/Face-Recognition-Based-Gate-Door-Opening-System
# ----------------------------------------------------------------------------------------------------------------------------#

import RPi.GPIO as GPIO
from gpiozero import Servo
import serial

from gpiozero.pins.pigpio import PiGPIOFactory

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2

from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
BuzzerPin = 26
GPIO.setup(BuzzerPin, GPIO.OUT)
GPIO.output(BuzzerPin, GPIO.HIGH)


servoPIN = 12
factory = PiGPIOFactory()

servo = Servo(12, min_pulse_width=0.7/1000, max_pulse_width=2.5/1000, pin_factory=factory)
servo.min()

Relay1 = 5
Relay2 = 6
GPIO.setup(Relay1, GPIO.OUT)
GPIO.output(Relay1, GPIO.HIGH)
GPIO.setup(Relay2, GPIO.OUT)
GPIO.output(Relay2, GPIO.HIGH)
      
data = serial.Serial(
                    port='/dev/ttyAMA0',
                    baudrate = 9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )
                    #timeout=1 # must use when using data.readline()
                    #)
lcd = LCD()
def safe_exit(signum, frame):
    exit(1)

def TwoBeep():
    GPIO.output(BuzzerPin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(BuzzerPin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(BuzzerPin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(BuzzerPin, GPIO.HIGH)
    
def LongBeep():
    GPIO.output(BuzzerPin, GPIO.LOW)
    time.sleep(1)
    GPIO.output(BuzzerPin, GPIO.HIGH)
    time.sleep(1)
    

def relay_on(pin):
    GPIO.output(pin, GPIO.HIGH)

def relay_off(pin):
    GPIO.output(pin, GPIO.LOW)
    
def relay_temp(pin):
    GPIO.output(pin, GPIO.LOW)
    time.sleep(2)
    GPIO.output(pin, GPIO.HIGH)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)
lcd.text("Welcome To", 1)
lcd.text("make2explore.com", 2)
time.sleep(2)
lcd.clear()
lcd.text("Face ID Based", 1)
lcd.text("Security System", 2)
servo.value = None;
time.sleep(2)
lcd.clear()

def face_detect():
	#Initialize 'currentname' to trigger only when a new person is identified.
	prevTime = 0
	currentname = "unknown"
	#Determine faces from encodings.pickle file model created from train_model.py
	encodingsP = "encodings.pickle"

	# load the known faces and embeddings along with OpenCV's Haar
	# cascade for face detection
	print("make2explore.com + face Detection Security System ...")
	data = pickle.loads(open(encodingsP, "rb").read())

	# initialize the video stream and allow the camera sensor to warm up
	# Set the ser to the followng
	# src = 0 : for the build in single web cam, could be your laptop webcam
	# src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
	vs = VideoStream(src=0,framerate=10).start()
	#vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)

	# start the FPS counter
	fps = FPS().start()

	# loop over frames from the video file stream
	while True:
		# grab the frame from the threaded video stream and resize it
		# to 500px (to speedup processing)
		faceD = False
		frame = vs.read()
		frame = imutils.resize(frame, width=500)
		# Detect the fce boxes
		boxes = face_recognition.face_locations(frame)
		# compute the facial embeddings for each face bounding box
		encodings = face_recognition.face_encodings(frame, boxes)
		names = []
		
		# loop over the facial embeddings
		for encoding in encodings:
			# attempt to match each face in the input image to our known
			# encodings
			matches = face_recognition.compare_faces(data["encodings"],
				encoding)
			name = "Unknown" #if face is not recognized, then print Unknown

			# check to see if we have found a match
			if True in matches:
				# find the indexes of all matched faces then initialize a
				# dictionary to count the total number of times each face
				# was matched
				matchedIdxs = [i for (i, b) in enumerate(matches) if b]
				counts = {}

				# loop over the matched indexes and maintain a count for
				# each recognized face face
				prevTime = time.time()
				for i in matchedIdxs:
					name = data["names"][i]
					counts[name] = counts.get(name, 0) + 1

				# determine the recognized face with the largest number
				# of votes (note: in the event of an unlikely tie Python
				# will select first entry in the dictionary)
				name = max(counts, key=counts.get)

				#If someone in your dataset is identified, print their name on the screen
				if currentname != name:
					faceD = True
					currentname = name
					if currentname == userName:
						lcd.clear()
						lcd.text("Welcome!!", 1)
						lcd.text(currentname, 2)
						print (currentname)
						print ("Valid User")
						servo.max()
						time.sleep(1)
						servo.min()
						time.sleep(1)
						servo.value = None;
						relay_temp(Relay2)
						time.sleep(1)
						break
					else:
						lcd.clear()
						lcd.text("Invalid User", 1)
						lcd.text("Access Denied", 2)
						print (currentname)
						print ("Invalid User")
						LongBeep()
						time.sleep(2)
						break
					#print(currentname)
					#time.sleep(2)				

			# update the list of names
			names.append(name)
			
		# loop over the recognized faces
		for ((top, right, bottom, left), name) in zip(boxes, names):
			# draw the predicted face name on the image - color is in BGR
			cv2.rectangle(frame, (left, top), (right, bottom),
				(0, 255, 225), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
				.8, (0, 255, 255), 2)

		# display the image to our screen
		cv2.imshow("Facial Recognition is Running", frame)
		key = cv2.waitKey(1) & 0xFF

		if faceD and time.time()-prevTime > 10:
			break

		# quit when 'q' key is pressed
		if key == ord("q"):
			break

		# update the FPS counter
		fps.update()

	# stop the timer and display FPS information
	fps.stop()
	print("[INFO] Real elapsed time: {:.2f}".format(time.time() - prevTime))
	print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()

try:     
   while 1:
         #x=data.readline()#print the whole data at once
         #x=data.read()#print single data at once
         userName = ""
         print ("Place the card")
         lcd.text("Place Your RFID", 1)
         lcd.text("Card on Reader", 2)
         time.sleep(1)
         x=data.read(12)
         x = str(x, 'UTF-8')
         lcd.clear()
         lcd.text("Scanning Card...", 1)
         lcd.text("Checking ID >>>", 2)
         time.sleep(1)
         
         if x=="0900963100AE":
             userName = "PA"
             #print ("Card No - ",x)
             #print ("Welcome User 1")
             lcd.clear()
             lcd.text("Authorized User", 1)
             lcd.text("Hello PA", 2)
             TwoBeep();
             relay_temp(Relay1)
             face_detect()
             #print (" ")
             
         elif x=="88001964699C":
             #print ("Card No - ",x)
             #print ("Welcome User 1")
             lcd.clear()
             lcd.text("Authorized User", 1)
             lcd.text("Hello Samihan", 2)
             TwoBeep();
             relay_temp(Relay1)
             #face_detect()
             #print (" ")
             
         elif x=="880013E5235D":
             #print ("Card No - ",x)
             #print ("Welcome User 1")
             lcd.clear()
             lcd.text("Authorized User", 1)
             lcd.text("Hello Raj", 2)
             TwoBeep();
             relay_temp(Relay1)
             #face_detect()
             #print (" ")
             
         elif x=="880013E5225C":
             #print ("Card No - ",x)
             #print ("Welcome User 1")
             lcd.clear()
             lcd.text("Authorized User", 1)
             lcd.text("Hello Vaidehi", 2)
             TwoBeep();
             relay_temp(Relay1)
             #face_detect()
             #print (" ")
             
         elif x=="880019646A9F":
             userName = "Mahesh"
             #print ("Card No - ",x)
             #print ("Welcome User 1")
             lcd.clear()
             lcd.text("Authorized User", 1)
             lcd.text("Hello Mahesh", 2)
             TwoBeep();
             relay_temp(Relay1)
             face_detect()
             #print (" ")
         else:
             #print ("Wrong Card.....")
             lcd.clear()
             lcd.text("Invalid RFID", 1)
             lcd.text("Unauthorized", 2)
             LongBeep();
             lcd.clear()
             lcd.text("    Access", 1)
             lcd.text("    Denied", 2)
             #print (" ")        
         
         #print x

except KeyboardInterrupt:
       servo.value = None;
       GPIO.cleanup()
       data.close()
