import datetime

# car class
class Car:
    def __init__(self, brand, model, fuel_capacity, fuel_level, state,is_moving = False, year=datetime.datetime.now()):
        self.brand = brand
        self.model = model     
        self.fuel_capacity = fuel_capacity   
        self.fuel_level = fuel_level
        self.state = state
        self.is_moving = is_moving
        self.yom = year

    def start(self):
        if self.fuel_capacity != 0 and self.state != "Started":
            self.state = "Started."
            self.is_moving = True
        elif self.is_moving == True:
            self.state = "Moving."
        
     
    def stop(self):
        if self.state != "Stopped":
            self.state = "Stopped."
            self.is_moving = False
        elif self.is_moving == True:
            self.state = "Moving"
        
    
    def refuel(self, fuel):
            self.fuel_capacity += fuel
            kms = self.fuel_capacity // 0.1
            # fuel level
            if self.fuel_capacity >= 0 and self.fuel_capacity < 10:
                self.fuel_level = "Warning"
                message = f"Fuel Capacity is {self.fuel_capacity}L.\nYou have {kms} kilometers to empty.\nFuel Level is {self.fuel_level}."
            elif self.fuel_capacity >= 10 and self.fuel_capacity < 15:
                self.fuel_level = "Low"
                message = f"Fuel Capacity is {self.fuel_capacity}L.\nYou have {kms} kilometers to empty.\nFuel Level is {self.fuel_level}."
            elif self.fuel_capacity >= 15 and self.fuel_capacity < 25:
                self.fuel_level = "E"
                message = f"Fuel Capacity is {self.fuel_capacity}L.\nYou have {kms} kilometers to empty.\nFuel Level is {self.fuel_level}."
            elif self.fuel_capacity >= 25:
                self.fuel_level = "F"
                message = f"Fuel Capacity is {self.fuel_capacity}L.\nYou have {kms} kilometers to empty.\nFuel Level is {self.fuel_level}."
            else:
                message = "Not valid"
      
            return message
    
    def drive(self):
        if self.is_moving == False: 
          message = "Start the vehicle."         
        elif self.fuel_capacity > 0: 
           self.is_moving == True       
           message = f"{self.brand} {self.model} is driving."
            
        return message
    
    def display_car_info(self):
      return f"""---CAR INFO---
Brand : {self.brand}
Model : {self.model}
Fuel Capacity : {self.fuel_capacity}
Fuel Level(Warning, Low, E, F) : {self.fuel_level}
Car Status : {self.state}
Is car moving : {self.is_moving}
Year of Make : {self.yom}\n"""
      
    
# tests
car_1 = Car("Mazda", "Demio", 20, "Low","Stopped")
print(car_1.is_moving)



car_1.drive()
car_1.stop()
rfl = car_1.refuel(12)
print(rfl)

info = car_1.display_car_info()
print(info)



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
Age : {self.age}"""
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
{super().display_info()}
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
{super().display_info()}
Teaching : {self.subject}
Monthly Salary : KES.{self.salary}\n"""
    
    
# tests
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


    

