#Importing other people's functions
import numpy as np  # math libraries
import cv2  # opencv itself
import socket # network communcation between pi and the computer

#This function allows us to fill a paramter when we are making trackbars
def nothing(x):
    pass

#All HaarCascades
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

#Setting up s***
cap = cv2.VideoCapture(0)
frame_height = 480
frame_width = 640
cap.set(3, frame_width)
cap.set(4, frame_height)

#Variables for getting location
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
curr_x = 0
curr_y = 0
ex, ey, eh, ew = 0,0,0,0
fx, fy, fh, fw = 0,0,0,0
focus_face = 0
focus_region = 0
eye_center = 0
center = False
left = False
right = False
data = ""
message_abroad = ""

#socket stuff
#s.connect(('192.168.1.22', 5560))
#message_abroad = ""

#Setting up Trackbars
cv2.namedWindow('Control Panel')  # makes a control panel
cv2.createTrackbar('Hue', 'Control Panel', 87, 180, nothing)  # default 0 205 255 69 8 12
cv2.createTrackbar('Sat', 'Control Panel', 132, 255, nothing)
cv2.createTrackbar('Val', 'Control Panel', 0, 255, nothing)
cv2.createTrackbar('Hrange', 'Control Panel', 51, 127, nothing)
cv2.createTrackbar('Srange', 'Control Panel', 122, 127, nothing)
cv2.createTrackbar('Vrange', 'Control Panel', 69, 127, nothing)

#When the program is running
while(True):

    #initializing the video feed variables
    ret, frame = cap.read()

    #Making the trackbars have actual value
    hue = cv2.getTrackbarPos('Hue', 'Control Panel')
    sat = cv2.getTrackbarPos('Sat', 'Control Panel')
    val = cv2.getTrackbarPos('Val', 'Control Panel')
    hrange = cv2.getTrackbarPos('Hrange', 'Control Panel')
    srange = cv2.getTrackbarPos('Srange', 'Control Panel')
    vrange = cv2.getTrackbarPos('Vrange', 'Control Panel')

    #Settting the pixels that have a certain value *cough*discrimination*cough*
    colorLower = (hue - hrange, sat - srange, val - vrange)
    colorUpper = (hue + hrange, sat + srange, val + vrange)

    #Detecting weird faces
    face = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=4, minSize=(50,50), maxSize=(200,200))
    if len(face):
        for(x, y, w, h) in face:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,255,255), 2)
            fx = x
            fy = y
            fh = h
            focus_face = frame[fy:fy+h, fx:fx+w]

            #Cutting your face in half
            fw = np.size(focus_face, 1)
            fww = int(fw/2)
            focus_region = frame[fy:fy+fh, fx:fx+fww]

            #Detecting eye...hope your not asian
            eyes = eye_cascade.detectMultiScale(focus_region, scaleFactor=1.3, minNeighbors=5)
            if len(eyes):
                for(ex,ey,ew,eh) in eyes:

                    #Drawing rectangle around the eye
                    cv2.rectangle(focus_region, (ex,ey), (ex+ew, ey+eh), (255,0,0), 2)
                    eye = focus_region[ey:ey+eh,ex:ex+ew]

                    #Cutting your eye in half
                    eye_center = ew/2

                    #Detecting your pupil
                    hsv = cv2.cvtColor(eye, cv2.COLOR_BGR2HSV)
                    mask = cv2.inRange(hsv, colorLower, colorUpper)
                    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

                    #If the program detects your pupil
                    if len(cnts) > 0:
                        #C is the biggest contour array
                        c = max(cnts, key=cv2.contourArea)

                        #Calculate the radius and center of circle
                        ((curr_x, curr_y), radius) = cv2.minEnclosingCircle(c)


                        #Determining whether you are looking left, right, center
                        cv2.circle(eye, (int(curr_x), int(curr_y)), int(radius), (255, 255, 0), 2, 2)
                        error = curr_x - eye_center

                        if(error > 1.5):
                            print("L")
                            message_abroad="left"
                            left = True
                            right = False
                            center = False
                        elif(error < -1.5):
                            print("R")
                            message_abroad ="right"
                            left = False
                            right = True
                            center = False
                        else:
                            print("F")
                            message_abroad = "center"
                            left = False
                            right = False
                            center = True
                        #print(error)
                        #s.send(message_abroad.encode())

                    #Displaying the masking, eye detection, and half of your face
                    cv2.imshow("roi", eye)
                    cv2.imshow("mask", mask)
                    cv2.imshow("two_face", focus_region)


    #Displaying overall feed
    cv2.putText(frame, message_abroad, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
    cv2.imshow("feed", frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()

