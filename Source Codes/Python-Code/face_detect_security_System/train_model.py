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

# Train Model

# import the necessary packages
from imutils import paths
import face_recognition
#import argparse
import pickle
import cv2
import os

# our images are located in the dataset folder
print("[INFO] start processing faces...")
imagePaths = list(paths.list_images("dataset"))

# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# extract the person name from the image path
	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	# load the input image and convert it from RGB (OpenCV ordering)
	# to dlib ordering (RGB)
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
	boxes = face_recognition.face_locations(rgb,
		model="hog")

	# compute the facial embedding for the face
	encodings = face_recognition.face_encodings(rgb, boxes)

	# loop over the encodings
	for encoding in encodings:
		# add each encoding + name to our set of known names and
		# encodings
		knownEncodings.append(encoding)
		knownNames.append(name)

# dump the facial encodings + names to disk
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()
