import numpy as np
class MotionVecP():
    """This class is for motion vector search"""
    def __init__(self, I, P):
        #Motion Position Matrix
        self.aroundMatrix = np.array([[-1,-1],[-1,0],[-1,1],[0,-1],[0,0],[0,1], [1,-1],[1,0],[1,1]])
        self.offset = 4
        self.Ref = I 
        self.Current = P
        self.defaultMBSize = 16
        self.stackReferencMat() #Extend the reference for compare


    def stackReferencMat(self):
        [rows, cols] = np.shape(self.Ref) #2 dimension

        self.Ref = np.vstack((self.Ref, np.zeros([self.offset,cols]))) #Extend Bottom
        self.Ref = np.vstack((np.zeros([self.offset,cols]), self.Ref)) #Extend Up
        self.Ref = np.hstack((self.Ref, np.zeros([rows+2*self.offset, self.offset]))) #Extend Right, added more rows
        self.Ref = np.hstack((np.zeros([rows+2*self.offset, self.offset]) ,self.Ref)) #Extend Left, added more rows

    def getMotionVecForOne(self, leftUpCorner):
        last = False
        minMad = 2**31 #Largest integer 
        localOffset = self.offset
        displacement = [0,0]
        mbSize = self.defaultMBSize
        orgCorner = np.array(leftUpCorner, copy=True)
        updatedCorner = np.array(leftUpCorner, copy=True)
        while last is not True:
            for i in range(9): #Nine Possible displacement
                displacement = localOffset*self.aroundMatrix[i]

                mad = self.getMad(orgCorner, displacement, mbSize)
                print mad
                if mad < minMad:
                    minMad = mad
                    updatedCorner += displacement #Update the corner

            if localOffset == 1:
                last = True

            localOffset /= 2

        return updatedCorner

    def getMotionVecForAll(self):
        [motionVecRows, motionVecCols] = np.shape(self.Current) #2 dimension
        motionVecRows /= self.defaultMBSize
        motionVecCols /= self.defaultMBSize
        motionVect = np.zeros([motionVecRows, motionVecCols,2])

        for i in range(motionVecRows):
            for j in range(motionVecCols):
                tmpCorner = [i*self.defaultMBSize, j*self.defaultMBSize]
                motionVect[i, j, :] = self.getMotionVecForOne(tmpCorner)

            

    def getMad(self, leftUpCornerCurrentFrame, displacement, mbSize):
        [row_0, col_0] = leftUpCornerCurrentFrame
        [row_d, col_d] = displacement + leftUpCornerCurrentFrame + [self.offset,self.offset]#
        P_part = self.Current[row_0:row_0+mbSize, col_0:col_0+mbSize] #P frame part
        #print "P_part"
        I_part = self.Ref[row_d:row_d+mbSize, col_d:col_d+mbSize] #I frame part

        mad = np.mean(abs(P_part-I_part)) # Mean Absolute
        return mad
        
        