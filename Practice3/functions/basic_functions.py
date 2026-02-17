# In Python, a function is defined using the def keyword, followed by a function name and parentheses:
def my_function():
  print("Hello from a function")

# To call a function, write its name followed by parentheses:
my_function()

# You can call the same function multiple times:
my_function()
my_function()
my_function()

# Valid function names:
# calculate_sum()
# _private_function()
# myFunction2()

# Without functions - repetitive code:
temp1 = 77
celsius1 = (temp1 - 32) * 5 / 9
print(celsius1)

temp2 = 95
celsius2 = (temp2 - 32) * 5 / 9
print(celsius2)

temp3 = 50
celsius3 = (temp3 - 32) * 5 / 9
print(celsius3)

# With functions, you write the code once and reuse it:
def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))

# pass statement
def calculate_sum():
  pass

calculate_sum()


# A variable created inside a function is available inside that function:
def myfunc1():
  x = 300
  print(x)

myfunc1()

# The local variable can be accessed from a function within the function:
def myfunc2():
  x = 300
  def myinnerfunc():
    print(x)
  myinnerfunc()

myfunc2()


# A variable created outside of a function is global and can be used by anyone:
x = 300
def myfunc3():
  print(x)

myfunc3()
print(x)

x = 300  # Global scope: this x is available everywhere

def myfunc4():
    # Local scope: this x is a NEW variable that exists only inside this function
    # This is called "Shadowing" — the local variable hides the global one
    x = 200  
    print(x) # Prints 200 (Python looks at the closest scope first)

myfunc4()

# Once the function ends, the local x is destroyed.
# We are back in the global scope where x is still 300.
print(x) # Prints 300


# If you use the global keyword, the variable belongs to the global scope:
def myfunc5():
  global x
  x = 300

myfunc5()

print(x)


# To change the value of a global variable inside a function, refer to the variable by using the global keyword:

x = 300

def myfunc6():
  global x
  x = 200

myfunc6()

print(x)


def myfunc7():
  x = "Jane" # Local to myfunc1 (outer variable)
  
  def myfunc8():
    # 'nonlocal' makes the function use the variable from the outer scope
    # instead of creating a new local one.
    nonlocal x 
    x = "hello" # This changes the 'x' in myfunc1
    
  myfunc8()
  return x # Returns "hello" because it was modified by myfunc2

print(myfunc7())

# The LEGB Rule
# Python follows the LEGB rule when looking up variable names, and searches for them in this order:

# Local - Inside the current function
# Enclosing - Inside enclosing functions (from inner to outer)
# Global - At the top level of the module
# Built-in - In Python's built-in namespace
# Example
# Understanding the LEGB rule:

x = "global"

def outer():
  x = "enclosing"
  def inner():
    x = "local"
    print("Inner:", x)
  inner()
  print("Outer:", x)

outer()
print("Global:", x)