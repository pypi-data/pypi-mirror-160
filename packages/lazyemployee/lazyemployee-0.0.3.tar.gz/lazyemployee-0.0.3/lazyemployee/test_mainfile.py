# from mainfile import Employee
# from mainfile import Employee,Accounting,Programmer,Sale

from lazyemployee.mainfile import Employee,Accounting,Programmer,Sale

def test():
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