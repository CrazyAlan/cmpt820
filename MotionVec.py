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

        self.Ref = np.vstack((self.Ref, np.zeros([self.offset*2,cols]))) #Extend Bottom
        self.Ref = np.vstack((np.zeros([self.offset*2,cols]), self.Ref)) #Extend Up
        self.Ref = np.hstack((self.Ref, np.zeros([rows+2*self.offset*2, self.offset*2]))) #Extend Right, added more rows
        self.Ref = np.hstack((np.zeros([rows+2*self.offset*2, self.offset*2]) ,self.Ref)) #Extend Left, added more rows

    def getMotionVecForOne(self, leftUpCorner):
        last = False
        minMad = 2**31 #Largest integer 
        localOffset = self.offset
        displacement = [0,0]
        mbSize = self.defaultMBSize
        orgCorner = np.array(leftUpCorner, copy=True)
        updatedCorner = np.array(leftUpCorner, copy=True)

        [row_0, col_0] = leftUpCorner
        P_part = self.Current[row_0:row_0+mbSize, col_0:col_0+mbSize]
        while last is not True:
            regCorner = np.array(updatedCorner, copy=True)
            for i in range(9): #Nine Possible displacement
                displacement = localOffset*self.aroundMatrix[i]
                #print(i,'i')
                #print(regCorner,'regCorner')
                mad = self.getMad(P_part, regCorner, displacement, mbSize)
                #print mad
                if mad < minMad:
                    #print('updatedCorner', updatedCorner)
                    minMad = mad
                    updatedCorner = regCorner + displacement #Update the corner

            if localOffset == 1:
                last = True

            localOffset /= 2
        #print updatedCorner-orgCorner
        return updatedCorner-orgCorner

    def getMotionVecForAll(self):
        [motionVecRows, motionVecCols] = np.shape(self.Current) #2 dimension
        motionVecRows /= self.defaultMBSize
        motionVecCols /= self.defaultMBSize
        motionVect = np.zeros([motionVecRows, motionVecCols,2])

        for i in range(motionVecRows):
            for j in range(motionVecCols):
                tmpCorner = [i*self.defaultMBSize, j*self.defaultMBSize]
                motionVect[i, j, :] = self.getMotionVecForOne(tmpCorner)

        return motionVect
            

    def getMad(self, P_part, leftUpCornerCurrentFrame, displacement, mbSize):
        #[row_0, col_0] = leftUpCornerCurrentFrame
        [row_d, col_d] = displacement + leftUpCornerCurrentFrame + [self.offset*2,self.offset*2]#
        
        #print "P_part"
        I_part = self.Ref[row_d:row_d+mbSize, col_d:col_d+mbSize] #I frame part
        #print('P_part',np.shape(P_part))
        mad = np.mean(abs(P_part-I_part)) # Mean Absolute
        return mad

    def recoverPfromI(self, IFrame, motionVector):
        mbSize = self.defaultMBSize

        recPFrame = np.zeros_like(IFrame) 
        [motionVecRows, motionVecCols] = np.shape(IFrame) #2 dimension
        motionVecRows /= mbSize
        motionVecCols /= mbSize
        for i in range(motionVecRows):
            for j in range(motionVecCols):
                #print motionVector[i,j,:]
                [rowPos, colPos] = motionVector[i,j,:] + [i*mbSize, j*mbSize] + [self.offset*2, self.offset*2]
                #print rowPos,rowPos+mbSize,colPos,colPos+mbSize
                recPFrame[i*mbSize:(i+1)*mbSize, j*mbSize:(j+1)*mbSize] = self.Ref[rowPos:rowPos+mbSize,colPos:colPos+mbSize]

        return recPFrame










        
        