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

# Capture Images for dataset

import cv2

name = 'PA' #replace with your name

cam = cv2.VideoCapture(0)

cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("press space to take a photo", 500, 300)

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("press space to take a photo", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "dataset/"+ name +"/image_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()

# ---------------------------------- make2explore.com-------------------------------------------------------------------------#