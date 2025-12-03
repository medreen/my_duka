import datetime

# school system
class Person:
    def __init__(self,n_id,f_name,l_name,age):
        self.national_id = n_id
        self.first_name = f_name
        self.last_name = l_name
        self.age = age

    def display_info(self):        
        if type(self.age) != int:
            message = "Age is not valid"
        else:
            message = f"""----INFORMATION---
National ID : {self.national_id}
First name : {self.first_name}
Last name : {self.last_name}
Age : {self.age} \n"""
        return message
    
class Student(Person):
    def __init__(self, n_id, s_id, f_name, l_name, age, course, duration, d_joined=datetime.datetime.now()):
        super().__init__(n_id, f_name, l_name, age)
        self.student_id = s_id
        self.course = course
        self.duration = duration
        self.date_joined = d_joined

    def display_info(self):
        return f"""---STUDENT DETAILS---
National ID : {self.national_id}
Student ID : {self.student_id}
First name : {self.first_name}
Last name : {self.last_name}
Age : {self.age}
Course : {self.course}
Duration : {self.duration}
Date Joined : {self.date_joined}\n"""
    
class Teacher(Person):
    def __init__(self, n_id, f_name, l_name, age, subject, salary):
        super().__init__(n_id, f_name, l_name, age)
        self.subject = subject
        self.salary = salary
        

    def display_info(self):
        return f"""---TEACHER DETAILS---
National ID : {self.national_id}
First name : {self.first_name}
Last name : {self.last_name}
Age : {self.age}
Teaching : {self.subject}
Monthly Salary : KES.{self.salary}\n"""

    
person_1 = Person("39402484","Jane", "Doe", 12)
print(person_1.age)

info = person_1.display_info()
print(info)

student_1 = Student("89702487", "90127", "Anne", "Kate", 12, "Architecture", "7 years")
print(student_1.date_joined)

info = student_1.display_info()
print(info)

teacher_1 = Teacher("89702487", "John", "Doe", 32, "Architecture", 90000)
print(teacher_1.salary)

info = teacher_1.display_info()
print(info)


    

