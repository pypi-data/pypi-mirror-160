class Person:
    def __init__(self,name,age):
        self.name = name
        self.age =  age

class Stu():
    def __init__(self,name,gender,stuid):
        self.name = name
        self.gender = gender
        self.stuid = stuid
    def stuid_add(self,a):
        return self.stuid+a
