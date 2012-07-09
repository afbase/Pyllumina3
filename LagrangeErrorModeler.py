"""Depracated"""

#from sage.all import *
#import random
#class LagrangeErrorModeler:
#    def __init__(self):
#        self.R = PolynomialRing(QQ,'x')
#        self.Range = [ 0.006065085,0.006752966,0.006889997,0.005806924,0.006805836,0.006090617,0.00585882,0.005771486,0.00600883,0.006184995,0.006507673,0.006705218,0.006993748,0.008411411,0.008301459,0.008794771,0.009186273,0.009589468,0.010324042,0.010934179,0.011882025,0.012618607,0.013554511,0.014738188,0.016239782,0.01811682,0.019900102,0.021542509,0.024181859,0.025834903,0.028442124,0.03194936,0.035342286,0.039713665,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.04548573,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735]
#        
#    def Interpolation(self,Points):
#        """
#        Inputs:
#        Points = a list of tuples representing points through which the polynomial returned by this function must pass.
#        """
#        return self.R.lagrange_polynomial(Points)
#        
#    def BuildMCONF(self,B):
#        """
#        Inputs:
#        B = The number of base pairs for the segment lengths of DNA
#        """
#        FileName = 'MCONF/%d_LangrangeErrorModel.mconf' %B
#        File = open(FileName,'w')
#        ErrorList = self.BuildErrorList(b=B)
#        File.write('SUBSTITUTION_ERROR\n')
#        for i in range(len(ErrorList)):
#            StringTemp = '%.10f\n'%ErrorList[i]
#            File.write(StringTemp)
#        File.close()
#    def BuildErrorList(self,a=1,b=100):
#        """
#        a = specifies the start of the domain
#        b = specifies the end of the domain
#        """
#        print 'b is now %d\n'%b
#        Length = float(b-a+1)
#        StepSize = Length/float(101)
#        NewDomain = [(a + StepSize*h) for h in range(101)]
#        UniqueDomain = self.uniq(NewDomain)
#        print 'length of NewDomain = %d'%len(NewDomain)
#        print 'length of UniqueDomain = %d'%len(UniqueDomain)
#        if UniqueDomain == NewDomain:
#            print 'hooray'
#            Pts = list()
#            for i in range(1,102):
#                pt = (NewDomain[i-1],self.Range[i-1])
#                Pts.append(pt)
#            f = self.Interpolation(Pts)
#            Errors = list()
#            for i in range(1,b+1):
#                Errors.append(f(i)+random.gauss(0,.00025))
#            return Errors
#        else:
#            print 'Domain Error'
#            print 'unique domain'
#            for i in range(len(UniqueDomain)):
#                print i,UniqueDomain[i]
#            print 'newdomain'
#            for i in range(len(NewDomain)):
#                print i,NewDomain[i]
#            return 0
#    def uniq(self,inlist): 
#        # order preserving
#        uniques = []
#        for item in inlist:
#            if item not in uniques:
#                uniques.append(item)
#        return uniques
#G = LagrangeErrorModeler()    
#for i in range(30,200):
#    G.BuildMCONF(i)