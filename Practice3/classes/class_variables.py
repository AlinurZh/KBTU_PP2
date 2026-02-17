# Create a private class property named __age:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.__age = age # Private property
p1 = Person("Emil", 25)
print(p1.name)
print(p1.__age) # This will cause an error


# Use a getter method to access a private property:
class Person:
  def __init__(self, name, age):
    self.name = name
    self.__age = age
  def get_age(self):
    return self.__age
p1 = Person("Tobias", 25)
print(p1.get_age())
class Person:
  def __init__(self, name, age):
    self.name = name
    self.__age = age
  def get_age(self):
    return self.__age
  def set_age(self, age):
    if age > 0:
      self.__age = age
    else:
      print("Age must be positive")
p1 = Person("Tobias", 25)
print(p1.get_age())
p1.set_age(26)
print(p1.get_age())


# Use encapsulation to protect and validate data:
class Student:
  def __init__(self, name):
    self.name = name
    self.__grade = 0
  def set_grade(self, grade):
    if 0 <= grade <= 100:
      self.__grade = grade
    else:
      print("Grade must be between 0 and 100")
  def get_grade(self):
    return self.__grade
  def get_status(self):
    if self.__grade >= 60:
      return "Passed"
    else:
      return "Failed"
student = Student("Emil")
student.set_grade(85)
print(student.get_grade())
print(student.get_status())


# Create a protected property:
class Person:
  def __init__(self, name, salary):
    self.name = name
    self._salary = salary # Protected property
p1 = Person("Linus", 50000)
print(p1.name)
print(p1._salary) # Can access, but shouldn't

class Calculator:
  def __init__(self):
    self.result = 0

  def __validate(self, num):
    if not isinstance(num, (int, float)):
      return False
    return True

  def add(self, num):
    if self.__validate(num):
      self.result += num
    else:
      print("Invalid number")

calc = Calculator()
calc.add(10)
calc.add(5)
print(calc.result)
# calc.__validate(5) # This would cause an error