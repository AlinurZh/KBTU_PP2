# Create a class named Person, use the __init__() method to assign values for name and age:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
p1 = Person("Emil", 36)
print(p1.name)
print(p1.age)
# Note: The __init__() method is called automatically every time the class is being used to create a new object.

# Why Use __init__()?
# Without the __init__() method, you would need to set properties manually for each object:
class Person:
  pass
p1 = Person()
p1.name = "Tobias"
p1.age = 25
print(p1.name)
print(p1.age)

# With __init__(), you can set initial values when creating the object:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
p1 = Person("Linus", 28)
print(p1.name)
print(p1.age)

# Set a default value for the age parameter:
class Person:
  def __init__(self, name, age=18):
    self.name = name
    self.age = age
p1 = Person("Emil")
p2 = Person("Tobias", 25)
print(p1.name, p1.age)
print(p2.name, p2.age)

# Create a Person class with multiple parameters:
class Person:
  def __init__(self, name, age, city, country):
    self.name = name
    self.age = age
    self.city = city
    self.country = country
p1 = Person("Linus", 30, "Oslo", "Norway")
print(p1.name)
print(p1.age)
print(p1.city)
print(p1.country)

# Use self to access class properties:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
  def greet(self):
    print("Hello, my name is " + self.name)
p1 = Person("Emil", 25)
p1.greet()


# The self parameter links the method to the specific object:
class Person:
  def __init__(self, name):
    self.name = name
  def printname(self):
    print(self.name)
p1 = Person("Tobias")
p2 = Person("Linus")
p1.printname()
p2.printname()

# It does not have to be named self, you can call it whatever you like, but it has to be the first parameter of any method in the class:
# Use the words myobject and abc instead of self:
class Person:
  def __init__(myobject, name, age):
    myobject.name = name
    myobject.age = age
  def greet(abc):
    print("Hello, my name is " + abc.name)
p1 = Person("Emil", 36)
p1.greet()

# Access multiple properties using self:
class Car:
  def __init__(self, brand, model, year):
    self.brand = brand
    self.model = model
    self.year = year
  def display_info(self):
    print(f"{self.year} {self.brand} {self.model}")
car1 = Car("Toyota", "Corolla", 2020)
car1.display_info()

# Call one method from another method using self:
class Person:
  def __init__(self, name):
    self.name = name
  def greet(self):
    return "Hello, " + self.name
  def welcome(self):
    message = self.greet()
    print(message + "! Welcome to our website.")
p1 = Person("Tobias")
p1.welcome()

# Create a class with properties:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
p1 = Person("Emil", 36)
print(p1.name)
print(p1.age)


# Access the properties of an object:
class Car:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model
car1 = Car("Toyota", "Corolla")
print(car1.brand)
print(car1.model)


# Change the age property:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
p1 = Person("Tobias", 25)
print(p1.age)
p1.age = 26
print(p1.age)


# Delete the age property:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
p1 = Person("Linus", 30)
del p1.age
print(p1.name) # This works
# print(p1.age) # This would cause an error


# Class Properties vs Object Properties:
# Class property vs instance property:
class Person:
  species = "Human" # Class property
  def __init__(self, name):
    self.name = name # Instance property
p1 = Person("Emil")
p2 = Person("Tobias")
print(p1.name)
print(p2.name)
print(p1.species)
print(p2.species)

# Change a class property:
class Person:
  lastname = ""
  def __init__(self, name):
    self.name = name
p1 = Person("Linus")
p2 = Person("Emil")
Person.lastname = "Refsnes"
print(p1.lastname)
print(p2.lastname)

# Add a new property to an object:
class Person:
  def __init__(self, name):
    self.name = name
p1 = Person("Tobias")
p1.age = 25
p1.city = "Oslo"
print(p1.name)
print(p1.age)
print(p1.city)


class Person:
  species = "Human"  # Original class property
  def __init__(self, name):
    self.name = name
# Adding a NEW class property from outside:
Person.country = "Unknown"
p1 = Person("Emil")
p2 = Person("Tobias")
print(p1.country)  # "Unknown"
print(p2.country)  # "Unknown"
# Modifying it:
Person.country = "Sweden"
print(p1.country)  # "Sweden"
print(p2.country)  # "Sweden"


