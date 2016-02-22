import numpy as np
import cv2

CONSTANT_VIDEO_PATH = "SampleVideo_360x240_50mb.mp4"
cap = cv2.VideoCapture(CONSTANT_VIDEO_PATH)
#i=1

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Encoding Part Start 
    


    #Encoding Part End
    

    # Display the Incoming frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #i += 1
    #cv2.imwrite("Frames/singleFrame"+str(i)+".tif", frame)




'''
while(True):
    #Do Thing to recover coded frame
    
    #Decoding Start 




    #Decoding End
    


    # Display the Incoming frame

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    pass
'''
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
