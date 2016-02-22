import numpy as np
class MotionVecP(object):
    """This class is for motion vector search"""
    def __init__(self, I, P):
        #Motion Position Matrix
        self.aroundMatrix = np.array([[-1,-1],[-1,0],[-1,1],[0,-1],[0,0],[0,1], [1,-1],[1,0],[1,1]])
        self.offset = 4
        self.Ref = I 
        self.Current = P
        self.defaultMBSize = 16
        self.Ref = self.stackReferencMat(self.Ref) #Extend the reference for compare


    def stackReferencMat(self, stackMat):
        [rows, cols] = np.shape(stackMat) #2 dimension

        stackMat = np.vstack((stackMat, np.zeros([self.offset*2,cols]))) #Extend Bottom
        stackMat = np.vstack((np.zeros([self.offset*2,cols]), stackMat)) #Extend Up
        stackMat = np.hstack((stackMat, np.zeros([rows+2*self.offset*2, self.offset*2]))) #Extend Right, added more rows
        stackMat = np.hstack((np.zeros([rows+2*self.offset*2, self.offset*2]) ,stackMat)) #Extend Left, added more rows
        return stackMat

    def getMotionVecForOne(self, refMat, leftUpCorner, madFlag = None):
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
                mad = self.getMad(refMat, P_part, regCorner, displacement, mbSize)
                #print mad
                if mad < minMad:
                    #print('updatedCorner', updatedCorner)
                    minMad = mad
                    updatedCorner = regCorner + displacement #Update the corner

            if localOffset == 1:
                last = True

            localOffset /= 2
        #print updatedCorner-orgCorner
        if madFlag == None:
            return updatedCorner-orgCorner
        else:
            return (updatedCorner-orgCorner,minMad)
        

    def getMotionVecForAll(self, refMat=None):
        if refMat is None:
            refMat = self.Ref
        [motionVecRows, motionVecCols] = np.shape(self.Current) #2 dimension
        motionVecRows /= self.defaultMBSize
        motionVecCols /= self.defaultMBSize
        motionVect = np.zeros([motionVecRows, motionVecCols,2])

        for i in range(motionVecRows):
            for j in range(motionVecCols):
                tmpCorner = [i*self.defaultMBSize, j*self.defaultMBSize]
                motionVect[i, j, :] = self.getMotionVecForOne(refMat, tmpCorner)

        return motionVect
            

    def getMad(self,refMat, P_part, leftUpCornerCurrentFrame, displacement, mbSize):
        #[row_0, col_0] = leftUpCornerCurrentFrame
        [row_d, col_d] = displacement + leftUpCornerCurrentFrame + [self.offset*2,self.offset*2]#
        
        #print "P_part"
        I_part = refMat[row_d:row_d+mbSize, col_d:col_d+mbSize] #I frame part
        #print('P_part',np.shape(P_part))
        mad = np.mean(abs(P_part-I_part)) # Mean Absolute
        return mad

    def recoverPfromI(self, IFrame, motionVector):
        
        refMat = np.array(IFrame, copy=True)
        refMat = self.stackReferencMat(refMat)
        
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
                recPFrame[i*mbSize:(i+1)*mbSize, j*mbSize:(j+1)*mbSize] = refMat[rowPos:rowPos+mbSize,colPos:colPos+mbSize]

        return recPFrame

    def diffFrame(self, IFrame):
        #print("Hello")
        motionVector = self.getMotionVecForAll()
        recoveredPFrame = self.recoverPfromI(IFrame, motionVector)
        diffResult = recoveredPFrame - self.Current

        return diffResult

class MotionVecB(MotionVecP):
    """docstring for MotionVecB"""
    def __init__(self, Ref1, Ref2, B):
        super(MotionVecB, self).__init__(Ref1,B)
        self.Ref2 = Ref2 
        self.Ref2 = self.stackReferencMat(self.Ref2)    

        self.MATCH_MAD_THREASH_HOLD = 10

    def getMotionVecForAll(self, refMat=None, madFlag=None):
        if refMat is None:
            refMat = self.Ref
        [motionVecRows, motionVecCols] = np.shape(self.Current) #2 dimension
        motionVecRows /= self.defaultMBSize
        motionVecCols /= self.defaultMBSize
        motionVect = np.zeros([motionVecRows, motionVecCols,2])
        minMad = np.zeros([motionVecRows, motionVecCols])

        for i in range(motionVecRows):
            for j in range(motionVecCols):
                tmpCorner = [i*self.defaultMBSize, j*self.defaultMBSize]
                (motionVect[i, j, :], minMad[i,j]) = self.getMotionVecForOne(refMat, tmpCorner, True)
                #print minMad
        if madFlag == None:
           return motionVect
        else:
            return (motionVect, minMad)

    def getTwoMotionVector(self):
        (motionVect1, minMad1) = self.getMotionVecForAll(None, True) # Get motion Vector for Ref 1
        (motionVect2, minMad2) = self.getMotionVecForAll(self.Ref2, True) #Get Motion Vector for Ref2
        #print sum(motionVect1-motionVect2)
        return (motionVect1, minMad1, motionVect2, minMad2)

    def diffFrame(self,Ref1, Ref2):
        (motionVect1, minMad1, motionVect2, minMad2) = self.getTwoMotionVector()

        recoveredImage1 = self.recoverPfromI(Ref1,motionVect1)
        recoveredImage2 = self.recoverPfromI(Ref2,motionVect1)
        #averageImage = (recoveredImage1+recoveredImage2)/2
        

        return (recoveredImage1, recoveredImage1)

            



           









        
        