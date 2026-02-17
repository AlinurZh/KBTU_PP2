# Create a class named MyClass, with a property named x:
class MyClass:
  x = 5
# Create an object named p1, and print the value of x:
p1 = MyClass()
print(p1.x)

# Delete the p1 object:
del p1

# Create three objects from the MyClass class:
p1 = MyClass()
p2 = MyClass()
p3 = MyClass()
print(p1.x)
print(p2.x)
print(p3.x)

# class definitions cannot be empty, but if you for some reason have a class definition with no content, put in the pass statement to avoid getting an error.
class Person:
   pass

# Access the inner class and create an object:
class Outer:
  def __init__(self):
    self.name = "Outer"
  class Inner:
    def __init__(self):
      self.name = "Inner"
    def display(self):
      print("Hello from inner class")
outer = Outer()
inner = outer.Inner()
inner.display()

class Computer:
  def __init__(self):
    self.cpu = self.CPU()
    self.ram = self.RAM()

  class CPU:
    def process(self):
      print("Processing data...")

  class RAM:
    def store(self):
      print("Storing data...")

computer = Computer()
computer.cpu.process()
computer.ram.store()