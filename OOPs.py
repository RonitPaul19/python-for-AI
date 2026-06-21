# Object oriented programming

#         Attributes
# class /
#       \ Methods


# First python class
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed


class Cat:
    def __init__(self, name, color):
        self.name = name
        self.color = color


# Creating objects
jerry = Dog(name="Jerry", breed="Labrador")

print(jerry.name)
print(jerry.breed)

# Creating objects
tom = Cat(name="Tom", color="white")

print(tom.name)
print(tom.color)
