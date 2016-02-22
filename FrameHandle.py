import numpy as np
import cv2
import MotionVec 


#Read All Frames
frames = []
for i in xrange(30,40):
	tmpFrame = cv2.imread("Frames/singleFrame"+str(i)+".tif")
	cv2.imshow('image', tmpFrame)
	frames.append(tmpFrame)






cv2.waitKey(0)
cv2.destroyAllWindows()




#	if cv2.waitKey(1) & 0xFF == ord('q'):
#		break
