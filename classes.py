class Person: 
    def __init__(self, name, age, height,address, is_married):
        self.name = name
        self.age = age
        self.height = height
        self.address = address
        self.is_married = is_married

    def greet(self):
        return f"Hi, my name is {self.name}."

person1 = Person("Alice", 25, "170cm", "St.Georgia", True)
person2 = Person("Ken", 34, "167cm", "Kimathi Street", False)

print(person1, "\n", person2)
print(type(person1), "\n", type(person2))
print(person1.greet(), "\n", person2.greet())
