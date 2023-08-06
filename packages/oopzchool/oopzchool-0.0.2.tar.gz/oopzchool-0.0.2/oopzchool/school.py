# _*_ coding: utf-8 _*_
class Student(): 
    def __init__(self,name,lastname):
        self.name = name
        self.lastname = lastname
        self.exp = 0
        self.lesson = 0
        self.vehicle = 'bus'
    @property    # This is special fn when reference fullname have no use ()
    def fullname(self):
        return ('{} {}'.format(self.name,self.lastname))
    def Coding(self):
        self.AddEXP()
        print('{} Code learning...'.format(self.fullname))
    def ShowEXP(self):
        print('{} point : {} exp lesson : {}'.format(self.name,self.exp,self.lesson))
    def AddEXP(self):
        self.exp += 10
        self.lesson +=1
    def __str__(self):
        return self.fullname
    def __repr__(self):     # repr == represent allstudent == object if we use __repr__ it gonna show fullname 
        return self.fullname
    def __add__(self,other):
        return self.exp + other.exp


class Tesla():
    def __init__(self):
        self.model = 'Tesla Model S'
    def SelfDriving(self,st):
        print('Auto drive is working...{} is going to home'.format(st.name))
    def __str__(self):
        return self.model



class SpecialStudent(Student):
    def __init__(self,name,lastname,father):
        super().__init__(name,lastname)
        self.father = father
        self.vehicle = Tesla()
        print("Do u know who is my father? My father is {}".format(self.father))
    def AddEXP(self):
        self.exp += 30
        self.lesson += 2

class Teacher:
    def __init__(self,fullname):
        self.fullname = fullname
        self.students = []
    def CheckStudent(self):
        print("----Teacher{}----".format(self.fullname))
        for i,st in enumerate(self.students):
            print('{}-->{} [{} exp][learn {} time]'.format(i+1,st.fullname,st.exp,st.lesson))
    def AddStudent(self,st):
        self.students.append(st)


# print('FILE:',__name__)
if __name__ == '__main__':
    # main()
    print("__name__")

    #Day 0
    print("----day 0----")
    allstudent=[]
    teacher1 = Teacher('Ada lovelace')
    teacher2 = Teacher('Bill Gates')
    print(teacher1.students)

    #Day 1
    print("----day 1----")
    st1 = Student('Albert','Einstein')
    allstudent.append(st1)
    teacher2.AddStudent(st1)
    print(st1.fullname)

    #Day 2
    print("----day 2----")
    st2 = Student('Steve','Jobs')
    allstudent.append(st2)
    teacher2.AddStudent(st2)
    print(st2.fullname)

    #Day 3
    print("----day 3----")
    for i in range(3):
        st1.Coding()
    st2.Coding()
    st1.ShowEXP()
    st2.ShowEXP()

    #Day 4
    print("----day 4----")

    stp1 = SpecialStudent('Thomas','Edison','Hitler')
    allstudent.append(stp1)
    teacher1.AddStudent(stp1)
    print(stp1.fullname)
    print("Teasher give me 20 point")
    stp1.exp = 20
    stp1.Coding()
    stp1.ShowEXP()

    #Day 5
    print("----day 5----")
    print("Hey student How do you go to your home?")
    print(allstudent)
    for st in allstudent:
        print("I : {} back home with {}".format(st.name,st.vehicle))
        #check ว่า object นี้เป็น class อะไร
        if isinstance(st,SpecialStudent):
            st.vehicle.SelfDriving(st)

    #Day 6
    print("----day 6----")
    teacher1.CheckStudent()
    teacher2.CheckStudent()
    print('Sum exp',st1+st2)