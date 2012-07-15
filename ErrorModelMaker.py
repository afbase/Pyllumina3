import random, math
from sys import float_info
from Logger import Logger
class ErrorModelMaker:
    def __init__(self,BuildInsertion = False,
                 BuildSubstitution = True,
                 BuildDeletion = False,
                 Variation = False,
                 FileName = None, 
                 N=100,
                 DeletionPoints=[0.00606508512067950,0.00675296642376962,0.00688999694872917,0.00580692396866418,0.00680583604896024,0.00609061670962565,0.00585881991631447,0.00577148570812953,0.00600882981888663,0.00618499536435559,0.00650767341787896,0.00670521809234427,0.00699374780209504,0.00841141135948587,0.00830145870238677,0.00879477131238090,0.00918627324146331,0.00958946761973615,0.01032404247887830,0.01093417870737930,0.01188202458790520,0.01261860720648550,0.01355451051017660,0.01473818756656830,0.01623978223562570,0.01811682034513980,0.01990010225231130,0.02154250858435480,0.02418185925226890,0.02583490296173980,0.02844212438633430,0.03194935989118780,0.03534228607419560,0.03971366519834600,0.04548573525944540,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660],
                 InsertionPoints=[0.00606508512067950,0.00675296642376962,0.00688999694872917,0.00580692396866418,0.00680583604896024,0.00609061670962565,0.00585881991631447,0.00577148570812953,0.00600882981888663,0.00618499536435559,0.00650767341787896,0.00670521809234427,0.00699374780209504,0.00841141135948587,0.00830145870238677,0.00879477131238090,0.00918627324146331,0.00958946761973615,0.01032404247887830,0.01093417870737930,0.01188202458790520,0.01261860720648550,0.01355451051017660,0.01473818756656830,0.01623978223562570,0.01811682034513980,0.01990010225231130,0.02154250858435480,0.02418185925226890,0.02583490296173980,0.02844212438633430,0.03194935989118780,0.03534228607419560,0.03971366519834600,0.04548573525944540,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660],
                 SubstitutionPoints =[0.00606508512067950,0.00675296642376962,0.00688999694872917,0.00580692396866418,0.00680583604896024,0.00609061670962565,0.00585881991631447,0.00577148570812953,0.00600882981888663,0.00618499536435559,0.00650767341787896,0.00670521809234427,0.00699374780209504,0.00841141135948587,0.00830145870238677,0.00879477131238090,0.00918627324146331,0.00958946761973615,0.01032404247887830,0.01093417870737930,0.01188202458790520,0.01261860720648550,0.01355451051017660,0.01473818756656830,0.01623978223562570,0.01811682034513980,0.01990010225231130,0.02154250858435480,0.02418185925226890,0.02583490296173980,0.02844212438633430,0.03194935989118780,0.03534228607419560,0.03971366519834600,0.04548573525944540,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660,0.05190994307855660]):
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
        return self.Variation
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
    
    def Normalize(self,X):
        Total = sum(X)
        NewVector = [(i/Total) for i in X]
        if sum(NewVector) != 1:
            Difference = math.sqrt(math.pow(1-sum(NewVector),2))
            Errors = Difference/float(len(X))
            NewVector = [i + Errors for i in NewVector]
        return NewVector
    def BuildErrorModel(self,FileName,N):
        Del = self.Normalize(self.GetDeletionPoints())
        Ins = self.Normalize(self.GetInsertionPoints())
        Sub = self.Normalize(self.GetSubstitutionPoints())
        #self.SetDeletionPoints(Del)
        #self.SetInsertionPoints(Ins)
        self.SetSubstitutionPoints(Sub)
        File = open(FileName,'w')
        self.BuildHeader(File)
        self.BuildSwitches(File)
        self.BuildDeletionErrors(File)
        self.BuildSubstitutionErrors(File)
        self.BuildInsertionErrors(File)
        File.close()
    def BuildHeader(self,FilePtr):
        Logr = Logger()
        TimeString = '#Date of Creation: %s\n'%Logr.TimeStamp2String(Logr.GetTimeStamp())
        strings = ['#Error Model written by Pyllumina 2.1\n',TimeString]
        FilePtr.writelines(strings)
    def BuildSwitches(self,FilePtr):
        BasePoints = ['G','T','A','C']
        for X1 in BasePoints:
            for X2 in BasePoints:
                Statement = '# (Set switch rates for %s following %s)\n' % (X1,X2)
                FilePtr.write(Statement) 
                for X3 in BasePoints:
                    SwitchValue = random.uniform(.3,.4+float_info.epsilon)
                    Statement = '%s(%s,%s) %f\n'%(X1,X2,X3,SwitchValue)
                    FilePtr.write(Statement)
    def BuildSubstitutionErrors(self,FilePtr):
        Points = self.GetSubstitutionPoints()
        LastPtIndex = len(Points)-1
        if self.GetBuildSubstitution() == True:
            Statement = '# Set Substitution Rates \n'
            FilePtr.write(Statement)
            Statement = 'SUBSTITUTION_ERROR\n'
            FilePtr.write(Statement)
            for i in range(self.GetN()):
                if i <= LastPtIndex and self.GetVariation() == False:
                    Statement = '%.17f\n'%Points[i]
                    FilePtr.write(Statement)
                elif i <= LastPtIndex and self.GetVariation() == True:
                    Statement = '%.17f\n'%(Points[i] + random.gauss(0,.00025))
                    FilePtr.write(Statement)
                elif i >= LastPtIndex and self.GetVariation() == False:
                    Statement = '%.17f\n'%Points[LastPtIndex]
                    FilePtr.write(Statement)
                else:
                    Statement = '%.17f\n'%(Points[LastPtIndex]+random.gauss(0,.00025))
                    FilePtr.write(Statement)
            return      
        else:
            return
#            Points = self.GetSubstitutionPoints()
#            LastPtIndex = len(Points)-1
#            BasePoints = ['G','T','A','C']
#            for j in BasePoints:
#                Statement = '# Set Substitution Rates for every %s \n'% j
#                FilePtr.write(Statement)
#                Statement = 'SUBSTITUTION_ERROR (%s)\n' % j
#                FilePtr.write(Statement)
#                for i in range(self.GetN()):
#                    if i <= LastPtIndex and self.GetVariation() == False:
#                        Statement = '%.47f\n'%Points[i]
#                        FilePtr.write(Statement)
#                    elif i <= LastPtIndex and self.GetVariation() == True:
#                        Statement = '%.47f\n'%(Points[i] + random.gauss(0,.00025))
#                        FilePtr.write(Statement)
#                    elif i >= LastPtIndex and self.GetVariation() == False:
#                        Statement = '%.47f\n'%Points[LastPtIndex]
#                        FilePtr.write(Statement)
#                    else:
#                        Statement = '%.47f\n'%(Points[LastPtIndex]+random.gauss(0,.00025))
#                        FilePtr.write(Statement)
#            return      
#        else:
#            return
    def BuildInsertionErrors(self,FilePtr):
        Points = self.GetInsertionPoints()
        LastPtIndex = len(Points)-1
        if self.GetBuildInsertion() == True:
            Statement = '# Set Insertion Rates\n'
            FilePtr.write(Statement)
            Statement = 'INSERTION_ERROR\n'
            FilePtr.write(Statement)
            for i in range(self.GetN()):
                if i <= LastPtIndex and self.GetVariation() == False:
                    Statement = '%.17f\n'%Points[i]
                    FilePtr.write(Statement)
                elif i <= LastPtIndex and self.GetVariation() == True:
                    Statement = '%.17f\n'%(Points[i] + random.gauss(0,.00025))
                    FilePtr.write(Statement)
                elif i >= LastPtIndex and self.GetVariation() == False:
                    Statement = '%.17f\n'%Points[LastPtIndex]
                    FilePtr.write(Statement)
                else:
                    Statement = '%.17f\n'%(Points[LastPtIndex]+random.gauss(0,.00025))
                    FilePtr.write(Statement)
            return      
        else:
            return
#        if self.GetBuildSubstitution() == True:
#            Points = self.GetInsertionPoints()
#            LastPtIndex = len(Points)-1
#            BasePoints = ['G','T','A','C']
#            for j in BasePoints:
#                Statement = '# Set Insertion Rates for every %s \n'% j
#                FilePtr.write(Statement)
#                Statement = 'INSERTION_ERROR (%s)\n' % j
#                FilePtr.write(Statement)
#                for i in range(self.GetN()):
#                    if i <= LastPtIndex and self.GetVariation() == False:
#                        Statement = '%.47f\n'%Points[i]
#                        FilePtr.write(Statement)
#                    elif i <= LastPtIndex and self.GetVariation() == True:
#                        Statement = '%.47f\n'%(Points[i] + random.gauss(0,.00025))
#                        FilePtr.write(Statement)
#                    elif i >= LastPtIndex and self.GetVariation() == False:
#                        Statement = '%.47f\n'%Points[LastPtIndex]
#                        FilePtr.write(Statement)
#                    else:
#                        Statement = '%.47f\n'%(Points[LastPtIndex]+random.gauss(0,.00025))
#                        FilePtr.write(Statement)
#            return      
#        else:
#            return
    def BuildDeletionErrors(self,FilePtr):
        Points = self.GetDeletionPoints()
        LastPtIndex = len(Points)-1
        if self.GetBuildDeletion() == True:
            Statement = '# Set Deletion Rates \n'
            FilePtr.write(Statement)
            Statement = 'DELETION_ERROR\n'
            FilePtr.write(Statement)
            for i in range(self.GetN()):
                if i <= LastPtIndex and self.GetVariation() == False:
                    Statement = '%.17f\n'%Points[i]
                    FilePtr.write(Statement)
                elif i <= LastPtIndex and self.GetVariation() == True:
                    Statement = '%.17f\n'%(Points[i] + random.gauss(0,.00025))
                    FilePtr.write(Statement)
                elif i >= LastPtIndex and self.GetVariation() == False:
                    Statement = '%.17f\n'%Points[LastPtIndex]
                    FilePtr.write(Statement)
                else:
                    Statement = '%.17f\n'%(Points[LastPtIndex]+random.gauss(0,.00025))
                    FilePtr.write(Statement)
            return      
        else:
            return
#        if self.GetBuildDeletion() == True:
#            Points = self.GetDeletionPoints()
#            LastPtIndex = len(Points)-1
#            BasePoints = ['G','T','A','C']
#            for j in BasePoints:
#                Statement = '# Set Deletion Rates for every %s \n'% j
#                FilePtr.write(Statement)
#                Statement = 'DELETION_ERROR (%s)\n' % j
#                FilePtr.write(Statement)
#                for i in range(self.GetN()):
#                    if i <= LastPtIndex and self.GetVariation() == False:
#                        Statement = '%.47f\n'%Points[i]
#                        FilePtr.write(Statement)
#                    elif i <= LastPtIndex and self.GetVariation() == True:
#                        Statement = '%.47f\n'%(Points[i] + random.gauss(0,.00025))
#                        FilePtr.write(Statement)
#                    elif i >= LastPtIndex and self.GetVariation() == False:
#                        Statement = '%.47f\n'%Points[LastPtIndex]
#                        FilePtr.write(Statement)
#                    else:
#                        Statement = '%.47f\n'%(Points[LastPtIndex]+random.gauss(0,.00025))
#                        FilePtr.write(Statement)
#            return      
#        else:
#            return