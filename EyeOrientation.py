#Importing other people's functions
import numpy as np  # math libraries
import cv2  # opencv itself

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

#Setting up Trackbars
cv2.namedWindow('Control Panel')  # makes a control panel
cv2.createTrackbar('Hue', 'Control Panel', 121, 180, nothing)  # default 0 205 255 69 8 12
cv2.createTrackbar('Sat', 'Control Panel', 139, 255, nothing)
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
            eyes = eye_cascade.detectMultiScale(focus_region, scaleFactor=1.6, minNeighbors=5)
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
                        eye_center_inL = eye_center + radius/2
                        eye_center_inR = eye_center - radius/2

                        if((curr_x > eye_center_inL)):
                            print("left")
                            left = True
                            right = False
                            center = False
                        if((curr_x) < (eye_center_inR)):
                            print("right")
                            left = False
                            right = True
                            center = False
                        if(curr_x < (eye_center_inL) and curr_x > (eye_center_inR)):
                            print("center")
                            left = False
                            right = False
                            center = True

                    #Displaying the masking, eye detection, and half of your face
                    cv2.imshow("roi", eye)
                    cv2.imshow("mask", mask)
                    cv2.imshow("two_face", focus_region)

       #Opening text file
        with open("orientation", 'r') as file:
            data = file.readlines()

        #Writing the program's result on that file
        if(left):
            data[0] = "left"
        elif(right):
            data[0] = "right"
        else:
            data[0] = "center"

        with open("orientation", "w") as file:
            file.writelines(data[0])

    #Displaying overall feed
    cv2.imshow("feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
file.close()
cv2.destroyAllWindows()

