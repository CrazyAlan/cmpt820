import numpy as np
import cv2
from MotionVec import *
from IntegerTransform import *
from ImageTransform import *
from Intra4by4Coding import *


frames = []
for i in xrange(30,40):
    tmpFrame = cv2.imread("Frames/singleFrame"+str(i)+".tif")
   # cv2.imshow('image', tmpFrame)
    frames.append(tmpFrame)

#Read Image Frames as double
IMT = ImageTransform()
rgbIm1 = IMT.im2double(frames[1])


#YUV transform
yuvIm1 = IMT.rgb2yuv(rgbIm1)
[Y, Cr, Cb] = IMT.chromaSub(yuvIm1)

#Intra Coding
IC = IntraCoding()
Y_r = IC.IntraCodingVec(Y)


#Integer Transform
IT = IntegerTransform()
IT.QuantizationMatrix(0)

#Vectorize
vecY = IMT.vecMat(Y, 4)

#Integer Transform
vecYIntTran = IT.EnIntegerTransformVec(vecY)


#DeInteger Transform
vecYIntDeTran = IT.DeIntegerTransformVec(vecYIntTran)

#Devectorize
vecYRec = IMT.dvecMat(np.shape(Y), vecYIntDeTran, 4)

print np.shape(vecYRec)
#Recover
yuvIm1Rec = IMT.chromaExpand(vecYRec, Cr, Cb)
rgbIm1Rec = IMT.yuv2rgb(yuvIm1)

'''
IFrame = frames[0][:,:,0]
BFrame1 = frames[1][:,:,0]
BFrame2 = frames[2][:,:,0]
PFrame = frames[3][:,:,0]


#Deal with P frame
mvP = MotionVecP(IFrame,PFrame)
motionVector = mvP.getMotionVecForAll()
recoveredPFrame = mvP.recoverPfromI(IFrame, motionVector)


#Deal with B1 frame
mvB1 = MotionVecB(IFrame,PFrame,BFrame1)
motionInfo =  mvB1.getTwoMotionVector()
recPFrame1 = mvB1.recoverPfromI(IFrame,PFrame,motionInfo)

#Deal with B2 frame
mvB2 = MotionVecB(IFrame,PFrame,BFrame2)
motionInfo =  mvB2.getTwoMotionVector()
recPFrame2 = mvB2.recoverPfromI(IFrame,PFrame,motionInfo)
'''







cv2.imshow('image', IMT.double2uintImage(Y_r))
cv2.waitKey(0)
cv2.destroyAllWindows()




#	if cv2.waitKey(1) & 0xFF == ord('q'):
#		break
