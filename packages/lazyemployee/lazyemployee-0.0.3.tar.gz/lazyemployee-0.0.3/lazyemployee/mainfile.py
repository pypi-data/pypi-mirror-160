class Employee():
    minsalary = 12000
    maxsalary = 300000
    companyname = 'gistda'
    def __init__(self,name,job,salary):
        self.name=name
        self.job = job
        self.salary = salary
    def detail(self):
        print("Name    : {}".format(self.name))
        print("job     : {}".format(self.job))
        print("salary  : {}".format(self.salary))
    def setname(self,newname):
        self.name=newname
    def setjob(self,newjob):
        self.job=newjob
    def setsalary(self,newsalary):
        self.salary=newsalary
    def getname(self):
        return self.name
    def getjob(self):
        return self.job
    def getsalary(self):
        return self.salary
    def CalculateSalary(self,bonus=0,overtime=0):
        return (self.salary+bonus+overtime)

class Accounting(Employee):
    Accouniden = "Accounting"
    def __init__(self,name,salary,age):
        super().__init__(name,self.Accouniden,salary)
        self.age = age
    def detail(self):
        super().detail()
        print('Age     : {}'.format(self.age))

class Programmer(Employee):
    programmeriden = "programmer"
    def __init__(self,name,salary,exp,skill):
        super().__init__(name,self.programmeriden,salary)
        self.exp = exp
        self.skill = skill
    def detail(self):
        super().detail()
        print("exp     : {}".format(self.exp))
        print("skill   : {}".format(self.skill))

class Sale(Employee):
    saleiden = "Sale"
    def __init__(self,name,salary,area):
        super().__init__(name,self.saleiden,salary)
        self.area = area
    def detail(self):
        super().detail()
        print("Area    : {}".format(self.area))

if __name__=="__main__":
    obj1= Employee('Tun','sleeper',2000)
    obj1.detail()
    print(obj1.CalculateSalary(2000,4000))
    print("\n")

    obj2= Accounting('Nan',20000,23)
    obj2.detail()
    print("\n")
   
    obj3= Programmer('Xan',20000,3,'Python')
    obj3.detail()
    print("\n")
    
    obj4= Sale('lin',20000,"A901")
    obj4.detail()
