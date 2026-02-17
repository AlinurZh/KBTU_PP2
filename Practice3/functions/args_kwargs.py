# Example
# Using **kwargs to accept any number of keyword arguments:

def my_function1(**kid):
  print("His last name is " + kid["lname"])

my_function1(fname = "Tobias", lname = "Refsnes")



def my_function2(**myvar):
  print("Type:", type(myvar))
  print("Name:", myvar["name"])
  print("Age:", myvar["age"])
  print("All data:", myvar)

my_function2(name = "Tobias", age = 30, city = "Bergen")



def my_function3(username, **details):
  print("Username:", username)
  print("Additional details:")
  for key, value in details.items():
    print(" ", key + ":", value)

my_function3("emil123", age = 25, city = "Oslo", hobby = "coding")



def my_function4(title, *args, **kwargs):
  print("Title:", title)
  print("Positional arguments:", args)
  print("Keyword arguments:", kwargs)

my_function4("User Info", "Emil", "Tobias", age = 25, city = "Oslo")


# Using * to unpack a list into arguments:
def my_function5(a, b, c):
  return a + b + c

numbers = [1, 2, 3]
result = my_function5(*numbers) # Same as: my_function(1, 2, 3)
print(result)


# my_function5(**{"fname": "Emil", "lname": "Refsnes"}) ----> my_function5(fname="Emil", lname="Refsnes")


# Using *args to accept any number of arguments:

def my_function6(*kids):
  print("The youngest child is " + kids[2])

my_function6("Emil", "Tobias", "Linus")


# Accessing individual arguments from *args:

def my_function7(*args):
  print("Type:", type(args))
  print("First argument:", args[0])
  print("Second argument:", args[1])
  print("All arguments:", args)

my_function7("Emil", "Tobias", "Linus")


def my_function8(greeting, *names):
  for name in names:
    print(greeting, name)

my_function8("Hello", "Emil", "Tobias", "Linus")

# A function that calculates the sum of any number of values:

def my_function9(*numbers):
  total = 0
  for num in numbers:
    total += num
  return total

print(my_function9(1, 2, 3))
print(my_function9(10, 20, 30, 40))
print(my_function9(5))


def my_function10(*numbers):
  if len(numbers) == 0:
    return None
  max_num = numbers[0]
  for num in numbers:
    if num > max_num:
      max_num = num
  return max_num

print(my_function10(3, 7, 2, 9, 1))

# Using * to unpack a list into arguments:

def my_function11(a, b, c):
  return a + b + c

numbers = [1, 2, 3]
result = my_function11(*numbers) # Same as: my_function(1, 2, 3)
print(result)

