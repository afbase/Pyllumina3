from numpy.random import multinomial
import math
import random
class SizeDistribution:
    def __init__(self,FileName = None,NumOfReads=None, Mean = None, Sigma = None):
        """
        Inputs:
        (Required) FileName = Name of File
        Mean = the average length of DNA Segments (integer)
        Sigma = the standard deviation of the DNA Segments (integer)
        NumOfReads = Number or reads for the distribution
        Objective of class: return a distribution file
        """
        self.SetFileName(FileName)
        self.SetNumOfReads(NumOfReads)
        self.SetMean(Mean)
        self.SetSigma(Sigma)
        self.BuildFile()
        
    def SetFileName(self,FN):
        self.FileName = FN
    def SetFolderName(self,FolderName):
        self.FolderName = FolderName
    def SetNumOfReads(self,NOR):
        self.NumOfReads = NOR
    def SetMean(self,AVG):
        self.Mean = AVG
    def SetSigma(self,Sigma):
        self.Sigma = Sigma
    
    def GetFolderName(self):
        return self.FolderName    
    def GetMean(self):
        return self.Mean
    def GetSigma(self):
        return self.Sigma
    def GetNumOfReads(self):
        return self.NumOfReads
    def GetFileName(self):
        return self.FileName
    
    def BuildFile(self):
        """
        This builds a Normal distribution of random vectors
        with +-3 sigma distribution
        """
        LowerBound= self.GetMean() - 3 * self.GetSigma()
        UpperBound= self.GetMean() + 3 * self.GetSigma()
        DistroDomain = [i for i in range(LowerBound,UpperBound+1)]
        NumOfReads = self.GetNumOfReads()
        SizeDistro = self.RandIntVec(len(DistroDomain),NumOfReads)
        FileName = self.GetFileName()
        Output = file(FileName,'w')
        for i in range(len(SizeDistro)):
            temp = '%d    %d\n'%(DistroDomain[i], SizeDistro[i])
            Output.write(temp)
        Output.close()
        
    def RandFloats(self,Size):
        Scalar = 1.0
        VectorSize = Size
        RandomVector = [random.random() for i in range(VectorSize)]
        RandomVectorSum = sum(RandomVector)
        RandomVector = [Scalar*i/RandomVectorSum for i in RandomVector]
        return RandomVector
    def RandIntVec(self,ListSize, ListSumValue, Distribution='Normal'):
        """
        Inputs:
        ListSize = the size of the list to return
        ListSumValue = The sum of list values
        Distribution = can be 'uniform' for uniform distribution, 'normal' for a normal distribution ~ N(0,1) with +/- 3 sigma  (default), or a list of size 'ListSize' or 'ListSize - 1' for an empirical (arbitrary) distribution. Probabilities of each of the p different outcomes. These should sum to 1 (however, the last element is always assumed to account for the remaining probability, as long as sum(pvals[:-1]) <= 1).  
        Output:
        A list of random integers of length 'ListSize' whose sum is 'ListSumValue'.
        """
        if type(Distribution) == list:
            DistributionSize = len(Distribution)
            if ListSize == DistributionSize or (ListSize-1) == DistributionSize:
                Values = multinomial(ListSumValue,Distribution,size=1)
                OutputValue = Values[0]
        elif Distribution.lower() == 'uniform': #I do not recommend this!!!! I see that it is not as random (at least on my computer) as I had hoped
            UniformDistro = [1/ListSize for i in range(ListSize)]
            Values = multinomial(ListSumValue,UniformDistro,size=1)
            OutputValue = Values[0]
        elif Distribution.lower() == 'normal':
            """
            Normal Distribution Construction....It's very flexible and hideous
            Assume a +-3 sigma range.  Warning, this may or may not be a suitable range for your implementation!
            If one wishes to explore a different range, then changes the LowSigma and HighSigma values
            """
            LowSigma    = -3#-3 sigma
            HighSigma   = 3#+3 sigma
            StepSize    = 1/(float(ListSize) - 1)
            ZValues     = [(LowSigma * (1-i*StepSize) +(i*StepSize)*HighSigma) for i in range(int(ListSize))]
            #Construction parameters for N(Mean,Variance) - Default is N(0,1)
            Mean        = 0
            Var         = 1
            #NormalDistro= [self.NormalDistributionFunction(Mean, Var, x) for x in ZValues]
            NormalDistro= list()
            for i in range(len(ZValues)):
                if i==0:
                    ERFCVAL = 0.5 * math.erfc(-ZValues[i]/math.sqrt(2))
                    NormalDistro.append(ERFCVAL)
                elif i ==  len(ZValues) - 1:
                    ERFCVAL = NormalDistro[0]
                    NormalDistro.append(ERFCVAL)
                else:
                    ERFCVAL1 = 0.5 * math.erfc(-ZValues[i]/math.sqrt(2))
                    ERFCVAL2 = 0.5 * math.erfc(-ZValues[i-1]/math.sqrt(2))
                    ERFCVAL = ERFCVAL1 - ERFCVAL2
                    NormalDistro.append(ERFCVAL)  
            print "Normal Distribution sum = %f"%sum(NormalDistro)
            Values = multinomial(ListSumValue,NormalDistro,size=1)
            OutputValue = Values[0]
        else:
            raise ValueError ('Cannot create desired vector')
        return OutputValue
    def NormalDistributionFunction(self,Mean, Sigma,X):
        TAU         = math.pi * 2.0#http://www.youtube.com/watch?v=jG7vhMMXagQ
        SQRTTAU     = math.sqrt(TAU)
        Coefficient = math.pow(Sigma*SQRTTAU, -1.0)
        Variance    = math.pow(Sigma,2.0)
        Dividend    = math.pow(X-Mean,2.0)
        Exponent    = -0.5 * (Dividend/Variance)
        Result      = Coefficient * math.exp(Exponent)
        return Result