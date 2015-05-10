import numpy as np
import cv2

url = 'http://192.168.1.5:8080/video?dummy=param.mjpg'

cap = cv2.VideoCapture(url)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corner = cv2.cornerHarris( gray, 2, 3, 0.04 )
    corner = cv2.dilate( corner, None )
    
    #frame[corner>0.01*corner.max()] = [0,0,255]
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
