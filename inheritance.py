class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "General Sound"
    
class Dog(Animal):
    def speak(self):
        return 'Barks' 
    
class Horse(Animal):
    def speak(self):
        return 'Neighs'
    
dog1 = Dog("Max")
horse1 = Horse("Paige")


