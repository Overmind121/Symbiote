import dlib
import cv2
import numpy as np
import socket 

def midpoint(p1, p2):
    return int((p1.x+p2.x)/2), int((p1.y+p2.y)/2)

def nothing(x):
    pass

cap = cv2.VideoCapture(1)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

cv2.namedWindow("Control Panel")
cv2.createTrackbar("Threshold", "Control Panel", 19, 255, nothing)

while(True):
    ret, frame = cap.read()

    thresh_val = cv2.getTrackbarPos("Threshold", "Control Panel")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        x = face.left()
        y = face.top()
        i = face.right()
        j = face.bottom()
        cv2.rectangle(frame, (x,y), (i,j), (0,255,0), 2)
        #print("face detected", len(faces))

        landmarks = predictor(gray, face)

        eye = np.array([(landmarks.part(36).x, landmarks.part(36).y),
                        (landmarks.part(37).x, landmarks.part(37).y),
                        (landmarks.part(38).x, landmarks.part(38).y),
                        (landmarks.part(39).x, landmarks.part(39).y),
                        (landmarks.part(40).x, landmarks.part(40).y),
                        (landmarks.part(41).x, landmarks.part(41).y)], np.int32)

        height, width, _ = frame.shape
        mask = np.zeros((height, width), np.uint8)
        cv2.polylines(mask, [eye], True, 255, 2)
        cv2.fillPoly(mask, [eye], 255)
        left_eye = cv2.bitwise_and(gray, gray, mask=mask)

        min_x = np.min(eye[:, 0])
        max_x = np.max(eye[:, 0])
        min_y = np.min(eye[:, 1])
        max_y = np.max(eye[:, 1])
        gray_eye = left_eye[min_y: max_y, min_x: max_x]
        _, threshold_eye = cv2.threshold(gray_eye, thresh_val, 255, cv2.THRESH_BINARY)

        threshold_eye = cv2.resize(threshold_eye, None, fx=5, fy=5)
        height, width = threshold_eye.shape

        left_side_threshold = threshold_eye[0: height, 0:int(width/2)]
        left_side_white =cv2.countNonZero(left_side_threshold)

        right_side_threshold = threshold_eye[0:height, int(width/2):width]
        right_side_white = cv2.countNonZero(right_side_threshold)

        extreme_left_threshold = threshold_eye[0:height, 0:int(width/4)]
        extreme_left_white = cv2.countNonZero(extreme_left_threshold)

        extreme_right_threshold = threshold_eye[0:height, int(width/1.25):width]
        extreme_right_white = cv2.countNonZero(extreme_right_threshold)

        center_white = extreme_right_white+extreme_left_white
        if(right_side_white > left_side_white and right_side_white>center_white):
            cv2.putText(frame, "right", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        elif(left_side_white > right_side_white and left_side_white > center_white):
            cv2.putText(frame, "left", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, "center", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)

        #cv2.putText(frame, str(right_side_white), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        #cv2.putText(frame, str(left_side_white), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("eye",left_eye)
        cv2.imshow("thresh", threshold_eye)
    cv2.imshow("bw", gray)
    cv2.imshow("feed", frame)
    print(frame.shape)
    if(cv2.waitKey(1) & 0xFF == ord ("q")):
        break
cv2.destroyAllWindows()