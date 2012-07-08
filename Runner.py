##this is an idea to build distribution size
import random
def RunInt():
    LowerBound = 600
    UpperBound = 1200
    VectorSize = 30
    RandomVector = [random.randint(LowerBound,UpperBound) for i in range(VectorSize)]
    RandomVectorSum = 1000*30
    #Sanity check that our RandomVectorSum is sensible/feasible
    if LowerBound*VectorSize <= RandomVectorSum and RandomVectorSum <= UpperBound*VectorSum:
        if sum(RandomVector) == RandomVectorSum:
            return RandomVector
        else:
            RunInt()       
RunInt()
import random
def RunFloat():
    Scalar = 1000
    VectorSize = 30
    RandomVector = [random.random() for i in range(VectorSize)]
    RandomVectorSum = sum(RandomVector)
    RandomVector = [Scalar*i/RandomVectorSum for i in RandomVector]
    return RandomVector
RunFloat()
    
    


