import math
class Association:
    print("asdd")
    def __init__(self, X , Y):
        self.X = X
        self.Y = Y
        self.XY = []
        self.X2 = []
        self.Y2 = []
        self.Corre = 0
    def calc(self):
        for i in range(0,len(self.X)):
                self.XY.append(self.X[i]*self.Y[i])
        
        for i in range(0,len(self.X)):
                self.X2.append(self.X[i]**2)
        
        for i in range(0,len(self.X)):
                self.Y2.append(self.Y[i]**2)
        return self.Y2 , self.XY ,self.X2 
    
    def CORRE(self):
        self.Corre =float ((len(self.X)*sum(self.XY))-(sum(self.X)*sum(self.Y)))/math.sqrt(((len(self.X)*sum(self.X2))-(sum(self.X)**2))*((len(self.Y)*sum(self.Y2))-(sum(self.Y)**2)))
        return self.Corre
        

asso1 = Association([2,1,3,2,4,5,3],[4,3,4,3,6,5,5]) 
asso1.calc()
asso1.CORRE()
print(asso1.X2)
print(asso1.Corre)