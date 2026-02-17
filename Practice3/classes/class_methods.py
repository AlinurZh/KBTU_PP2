# Methods are functions that belong to a class. They define the behavior of objects created from the class.
# Create a method in a class:
class Person:
  def __init__(self, name):
    self.name = name
  def greet(self):
    print("Hello, my name is " + self.name)
p1 = Person("Emil")
p1.greet()



# Create a method with parameters:
class Calculator:
  def add(self, a, b):
    return a + b
  def multiply(self, a, b):
    return a * b
calc = Calculator()
print(calc.add(5, 3))
print(calc.multiply(4, 7))



# A method that accesses object properties:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
  def get_info(self):
    return f"{self.name} is {self.age} years old"
p1 = Person("Tobias", 28)
print(p1.get_info())



# A method that changes a property value:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
  def celebrate_birthday(self):
    self.age += 1
    print(f"Happy birthday! You are now {self.age}")
p1 = Person("Linus", 25)
p1.celebrate_birthday()
p1.celebrate_birthday()



# The __str__() method is a special method that controls what is returned when the object is printed:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
  def __str__(self):
    return f"{self.name} ({self.age})"
p1 = Person("Tobias", 36)
print(p1)



# Create multiple methods in a class:
class Playlist:
  def __init__(self, name):
    self.name = name
    self.songs = []
  def add_song(self, song):
    self.songs.append(song)
    print(f"Added: {song}")
  def remove_song(self, song):
    if song in self.songs:
      self.songs.remove(song)
      print(f"Removed: {song}")
  def show_songs(self):
    print(f"Playlist '{self.name}':")
    for song in self.songs:
      print(f"- {song}")
my_playlist = Playlist("Favorites")
my_playlist.add_song("Bohemian Rhapsody")
my_playlist.add_song("Stairway to Heaven")
my_playlist.show_songs()


# Delete a method from a class:
class Person:
  def __init__(self, name):
    self.name = name
  def greet(self):
    print("Hello!")
p1 = Person("Emil")
del Person.greet
p1.greet() # This will cause an error

# For strings len() returns the number of characters:
# ExampleGet your own Python Server
x = "Hello World!"
print(len(x))

# For tuples len() returns the number of items in the tuple:
mytuple = ("apple", "banana", "cherry")
print(len(mytuple))

# For dictionaries len() returns the number of key/value pairs in the dictionary:
thisdict = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
print(len(thisdict))

# Different classes with the same method:

class Car:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model

  def move(self):
    print("Drive!")

class Boat:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model

  def move(self):
    print("Sail!")

class Plane:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model

  def move(self):
    print("Fly!")

car1 = Car("Ford", "Mustang")       #Create a Car object
boat1 = Boat("Ibiza", "Touring 20") #Create a Boat object
plane1 = Plane("Boeing", "747")     #Create a Plane object

for x in (car1, boat1, plane1):
  x.move()


# Create a class called Vehicle and make Car, Boat, Plane child classes of Vehicle:
class Vehicle:
  def __init__(self, brand, model):
    self.brand = brand
    self.model = model

  def move(self):
    print("Move!")

class Car(Vehicle):
  pass

class Boat(Vehicle):
  def move(self):
    print("Sail!")

class Plane(Vehicle):
  def move(self):
    print("Fly!")

car1 = Car("Ford", "Mustang")       #Create a Car object
boat1 = Boat("Ibiza", "Touring 20") #Create a Boat object
plane1 = Plane("Boeing", "747")     #Create a Plane object

for x in (car1, boat1, plane1):
  print(x.brand)
  print(x.model)
  x.move()