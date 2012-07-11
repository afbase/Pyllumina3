import random
from sys import float_info
from Logger import Logger
class ErrorModelMaker:
    def __init__(self,BuildInsertion = True,BuildSubstitution = True,BuildDeletion = True,Variation = False,FileName = None, N=100,DeletionPoints=[0.00606508512067950,0.00675296642376962,0.00688999694872917,0.00580692396866418,0.00680583604896024,0.00609061670962565,0.00585881991631447,0.00577148570812953,0.00600882981888663,0.00618499536435559,0.00650767341787896,0.00670521809234427,0.00699374780209504,0.00841141135948587,0.00830145870238677,0.00879477131238090,0.00918627324146331,0.00958946761973615,0.01032404247887830,0.01093417870737930,0.01188202458790520,0.01261860720648550,0.01355451051017660,0.01473818756656830,0.01623978223562570,0.01811682034513980,0.01990010225231130,0.02154250858435480,0.02418185925226890,0.02583490296173980,0.02844212438633430,0.03194935989118780,0.03534228607419560,0.03971366519834600,0.04548573525944540,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660],InsertionPoints=[0.00606508512067950,0.00675296642376962,0.00688999694872917,0.00580692396866418,0.00680583604896024,0.00609061670962565,0.00585881991631447,0.00577148570812953,0.00600882981888663,0.00618499536435559,0.00650767341787896,0.00670521809234427,0.00699374780209504,0.00841141135948587,0.00830145870238677,0.00879477131238090,0.00918627324146331,0.00958946761973615,0.01032404247887830,0.01093417870737930,0.01188202458790520,0.01261860720648550,0.01355451051017660,0.01473818756656830,0.01623978223562570,0.01811682034513980,0.01990010225231130,0.02154250858435480,0.02418185925226890,0.02583490296173980,0.02844212438633430,0.03194935989118780,0.03534228607419560,0.03971366519834600,0.04548573525944540,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660],SubstitutionPoints = [ 0.006065085,0.006752966,0.006889997,0.005806924,0.006805836,0.006090617,0.00585882,0.005771486,0.00600883,0.006184995,0.006507673,0.006705218,0.006993748,0.008411411,0.008301459,0.008794771,0.009186273,0.009589468,0.010324042,0.010934179,0.011882025,0.012618607,0.013554511,0.014738188,0.016239782,0.01811682,0.019900102,0.021542509,0.024181859,0.025834903,0.028442124,0.03194936,0.035342286,0.039713665,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.04548573,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735,0.045485735]):
        """
        BuildInsertion                     = Do you want to build Insertion Errors?
        BuildDeletion                      = Do you want to build Deletion Errors?
        BuildSubstitution                  = Do you want to build Sustitution Errors?
        (Required) Variation               = Do you want to randomly vary the Error Rates
        (Required)FileName                 = The name of the mconf file for the error model
        DeletionPoints                     = The array of deletion rate values
        InsertionPoints                    = The array of insertion rate values
        SubstitutionPoints                 = The array of Substituion rate values
        """
        self.SetDeletionPoints(DeletionPoints)
        self.SetInsertionPoints(InsertionPoints)
        self.SetSubstitutionPoints(SubstitutionPoints)
        self.SetN(N)
        self.SetBuildInsertion(BuildInsertion)
        self.SetBuildSubstitution(BuildSubstitution)
        self.SetBuildDeletion(BuildDeletion)
        self.SetVariation(Variation)
        if FileName == None:
            FileName = 'ErrorModel-%dbp.mconf' %self.N
        self.BuildErrorModel(FileName,self.N)
    
    def SetDeletionPoints(self,Pts):
        self.DeletionPoints = Pts
    def SetInsertionPoints(self,Pts):
        self.InsertionPoints = Pts
    def SetSubstitutionPoints(self,Pts):
        self.SubstitutionPoints = Pts
    def SetN(self,N):
        self.N= N
    def SetVariation(self,X):
        self.Variation = X
    def SetBuildInsertion(self,Bool):
        self.BuildInsertion = Bool
    def SetBuildSubstitution(self,Bool):
        self.BuildSubstitution = Bool
    def SetBuildDeletion(self,Bool):
        self.BuildDeletion = Bool
            
    def GetVariation(self):
        return self.Vartiation
    def GetDeletionPoints(self):
        return self.DeletionPoints
    def GetInsertionPoints(self):
        return self.InsertionPoints
    def GetSubstitutionPoints(self):
        return self.SubstitutionPoints
    def GetN(self):
        return self.N
    def GetBuildInsertion(self):
        return self.BuildInsertion
    def GetBuildSubstitution(self):
        return self.BuildSubstitution
    def GetBuildDeletion(self):
        return self.BuildDeletion
    
    def BuildErrorModel(self,FileName,N):
        File = open(FileName,'w')
        self.BuildHeader(File)
        self.BuildSwitches(File)
        self.BuildDeletionErrors(File)
        self.BuildsubstitutionErrors(File)
        self.BuildInsertionErrors(File)
        File.close()
    def BuildHeader(self,FilePtr):
        Logr = Logger()
        TimeString = '#Date of Creation: %s'%Logr.TimeStamp2String(Logr.GetTimeStamp())
        strings = ['#Error Model written by Pyllumina 2.1',TimeString]
        FilePtr.writelines(strings)
    def BuildSwitches(self,FilePtr):
        BasePoints = ['G','T','A','C']
        for X1 in BasePoints:
            for X2 in BasePoints:
                Statement = '# (Set switch rates for %s following %s)\n' % X1,X2
                FilePtr.write(Statement) 
                for X3 in BasePoints:
                    SwitchValue = random.uniform(.3,.4+float_info.epsilon)
                    Statement = '%s(%s,%s) %f\n'%X1,X2,X3,SwitchValue
                    FilePtr.write(Statement)
    def BuildSubstitutionErrors(self,FilePtr):
        if self.GetBuildSubstitution() == True:
            Points = self.GetSubstitutionPoints()
            LastPtIndex = len(Points)-1
            BasePoints = ['G','T','A','C']
            for j in BasePoints:
                Statement = '# Set Substitution Rates for every %s'% j
                FilePtr.write(Statement)
                Statement = 'SUBSTITUTION_ERROR (%s)\n' % j
                FilePtr.write(Statement)
                for i in range(self.GetN()):
                    if i <= LastPtIndex and self.GetVariation() == False:
                        Statement = '%f\n'%Points[i]
                        FilePtr.write(Statement)
                    elif i <= LastPtIndex and self.GetVariation() == True:
                        Statement = '%f\n'%(Points[i] + random.gauss(0,.00025))
                        FilePtr.write(Statement)
                    elif i >= LastPtIndex and self.GetVariation() == False:
                        Statement = '%f\n'%Points[LastPtIndex]
                        FilePtr.write(Statement)
                    else:
                        Statement = '%f\n'%(Points[LastPtIndex]+random.gauss(0,.00025))
                        FilePtr.write(Statement)
            return      
        else:
            return
    def BuildInsertionErrors(self,FilePtr):
        if self.GetBuildSubstitution() == True:
            Points = self.GetInsertionPoints()
            LastPtIndex = len(Points)-1
            BasePoints = ['G','T','A','C']
            for j in BasePoints:
                Statement = '# Set Insertion Rates for every %s'% j
                FilePtr.write(Statement)
                Statement = 'INSERTION_ERROR (%s)\n' % j
                FilePtr.write(Statement)
                for i in range(self.GetN()):
                    if i <= LastPtIndex and self.GetVariation() == False:
                        Statement = '%f\n'%Points[i]
                        FilePtr.write(Statement)
                    elif i <= LastPtIndex and self.GetVariation() == True:
                        Statement = '%f\n'%(Points[i] + random.gauss(0,.00025))
                        FilePtr.write(Statement)
                    elif i >= LastPtIndex and self.GetVariation() == False:
                        Statement = '%f\n'%Points[LastPtIndex]
                        FilePtr.write(Statement)
                    else:
                        Statement = '%f\n'%(Points[LastPtIndex]+random.gauss(0,.00025))
                        FilePtr.write(Statement)
            return      
        else:
            return
    def BuildDeletionErrors(self,FilePtr):
        if self.GetBuildDeletion() == True:
            Points = self.GetDeletionPoints()
            LastPtIndex = len(Points)-1
            BasePoints = ['G','T','A','C']
            for j in BasePoints:
                Statement = '# Set Deletion Rates for every %s'% j
                FilePtr.write(Statement)
                Statement = 'DELETION_ERROR (%s)\n' % j
                FilePtr.write(Statement)
                for i in range(self.GetN()):
                    if i <= LastPtIndex and self.GetVariation() == False:
                        Statement = '%f\n'%Points[i]
                        FilePtr.write(Statement)
                    elif i <= LastPtIndex and self.GetVariation() == True:
                        Statement = '%f\n'%(Points[i] + random.gauss(0,.00025))
                        FilePtr.write(Statement)
                    elif i >= LastPtIndex and self.GetVariation() == False:
                        Statement = '%f\n'%Points[LastPtIndex]
                        FilePtr.write(Statement)
                    else:
                        Statement = '%f\n'%(Points[LastPtIndex]+random.gauss(0,.00025))
                        FilePtr.write(Statement)
            return      
        else:
            return