from sage.gsl.all import spline
from sage.all import *
import random
class SplineInterpolation:
    def __init__(self,N = float(100),Points = [ 0.006065085,0.006752966,0.006889997,0.005806924,0.006805836,0.006090617,0.00585882,0.005771486,0.00600883,0.006184995,0.006507673,0.006705218,0.006993748,0.008411411,0.008301459,0.008794771,0.009186273,0.009589468,0.010324042,0.010934179,0.011882025,0.012618607,0.013554511,0.014738188,0.016239782,0.01811682,0.019900102,0.021542509,0.024181859,0.025834903,0.028442124,0.03194936,0.035342286,0.039713665,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.04548573,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735]):
        self.SetPoints(Points)
        self.SetN(N)
        #Build Spline
        Inter = self.BuildSpline()
        self.SetSpline(Inter)
        #Build N Interpolation points
        InterpolatedPts = self.BuildInterpolatedPoints()
        self.SetInterpolationPoints(InterpolatedPts)
        #Build SolutionSpace
        Domain = [(i+1) for i in range(self.GetN())]
        SolnSpace = self.BuildSolutionSpace(Domain,self.GetInterpolationPoints())
        self.SetSolutionSpace(SolnSpace)
        #Build Varied Points
        VariedPts = self.BuildVariedPoints(self.GetInterpolationPoints())
        self.SetVariedPoints(VariedPts)
    
    def SetVariedPoints(self,X):
        self.VariedPoints = X
    def SetInterpolationPoints(self,Pts):
        self.InterpolationPoints = Pts
    def SetSolutionSpace(self,space):
        self.SolutionSpace = space
    def SetPoints(self,Pts):
        self.Points = Pts
    def SetN(self,N):
        self.N= N
    def SetSpline(self,Spl):
        self.Spline = Spl

    def GetSolutionSpace(self):
        return self.SolutionSpace    
    def GetVariedPoints(self):
        return self.VariedPoints
    def GetInterpolationPoints(self):
        return self.InterpolationPoints
    def GetPoints(self):
        return self.Points 
    def GetN(self):
        return self.N
    def GetSpline(self):
        return self.Spline
    
    def BuildSpline(self):
        #StepSize = 1.0 / (float(self.GetN()) - float(1))
        #SamplePts = [( 1.0 + h * StepSize * len(self.GetPoints())) for h in range(self.GetN())]
        SolnSpace = [(float(i+1),float(self.GetPoints()[i])) for i in range(len(self.GetPoints()))]
        Interpolation = spline(SolnSpace)
        return Interpolation
    def BuildInterpolatedPoints(self):
        StepSize = 1.0 / (float(self.GetN()) - float(1))
        SamplePts = [( 1.0 + h * StepSize * len(self.GetPoints())) for h in range(self.GetN())]
        Interpolation = self.GetSpline()
        SampleRange = [Interpolation(x) for x in SamplePts]
        return SampleRange
    def BuildVariedPoints(self, InterPts):
        ModifiedPts = [ (float(x) + random.gauss(0,.00025)) for x in InterPts]
        return ModifiedPts
    def BuildSolutionSpace(self, Domain, Range):
        SolnSpace = [(float(Domain[i]),float(Range[i])) for i in range(len(Range))]
        return SolnSpace
    def BuildVariedSolutionSpace(self, Domain, Range):
        SolnSpace = [(float(Domain[i]) ,float(Range[i])+ random.gauss(0,.00025)) for i in range(len(Range))]
        return SolnSpace

"""
Testing
"""
K = SplineInterpolation(N=1000)
JRange = K.GetPoints()
JDomain = [(i+1) for i in range(len(JRange))]
J = K.BuildSolutionSpace(JDomain, JRange)
Q = list_plot(J,color='green')
P = list_plot(K.GetSolutionSpace())
(P+Q).plot()