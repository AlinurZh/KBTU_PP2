# Parameters vs Arguments
# A function with one argument:

def my_function1(fname): # <----- parameter
  print(fname + " Refsnes")

my_function1("Emil")  # <----- argument
my_function1("Tobias") # <----- argument
my_function1("Linus") # <----- argument

# This function expects 2 arguments, and gets 2 arguments::

def my_function2(fname, lname):
  print(fname + " " + lname)

my_function2("Emil", "Refsnes")

# Default Parameter Values
def my_function3(name = "friend"):
  print("Hello", name)

my_function3("Emil")
my_function3("Tobias")
my_function3()
my_function3("Linus")

# Keyword Arguments
# You can send arguments with the key = value syntax.(The order doesn't matter)
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function(name = "Buddy", animal = "dog")

# Mixing Positional and Keyword Arguments
def my_function4(animal, name, age):
  print("I have a", age, "year old", animal, "named", name)

my_function4("dog", age = 5, name = "Buddy")

# All Positional-Only
def my_function5(a, b, /):
    return a + b

my_function5(10, 20)      # Valid: values passed positionally
# my_function(a=10, b=20) or my_function(b=10, a=20)  # Invalid: TypeError


# Keyword-Only Arguments
def multiply(*, x, y):
    # x and y must be passed by name
    return x * y

# Valid call
result = multiply(y=5, x=10) # or multiply(x=5, y=10)
print(result) # Output: 50

# Invalid call (TypeError: multiply() takes 0 positional arguments but 2 were given)
# result = multiply(5, 10)


# Combining Positional-Only and Keyword-Only
def my_function6(a, b, /, *, c, d):
  return a + b + c + d

result = my_function6(5, 10, c = 15, d = 20)
print(result)


# Another example of Combining Positional-Only + Keyword-Only + pos_or_kwd
def mixed_args(pos_only, /, pos_or_kwd, *, kwd_only):
    print(f"Positional-only: {pos_only}, Positional-or-keyword: {pos_or_kwd}, Keyword-only: {kwd_only}")

mixed_args(1, 2, kwd_only=3)        # Valid
mixed_args(1, pos_or_kwd=2, kwd_only=3) # Valid
# mixed_args(pos_only=1, 2, kwd_only=3) # Invalid: TypeError
# mixed_args(1, 2, 3)                   # Invalid: TypeError (missing keyword-only)

# Lambda Functions 
# lambda arguments : expression
x = lambda a : a + 10
print(x(5))

x = lambda a, b : a * b
print(x(5, 6))

x = lambda a, b, c : a + b + c
print(x(5, 6, 2))

###################################################################################

# In Python, functions can RETURN other functions.
# This makes the variable 'mydoubler' a function object itself.

def myfunc(n):
    # Returns a lambda function as an OBJECT
    return lambda a : a * n

# 1. We call myfunc(2)
# 2. It creates a lambda that "remembers" n = 2
# 3. mydoubler now POINTS to that lambda function
mydoubler = myfunc(2)

# Since mydoubler is a function, we use () to execute it
result = mydoubler(10) # 10 * 2 = 20

# When you write: mydoubler = myfunc(2)

# 1. The code inside 'myfunc' is executed.
# 2. It reaches the line: return lambda a : a * n.
# 3. A "live" function object (the lambda) is created.
# 4. This object is "thrown" out of 'myfunc' as the result (return value).
# 5. The variable 'mydoubler' simply catches this object and starts pointing to it.

# Now 'mydoubler' is not a number; it is a reference to a function. 
# That’s why you can "call" it by adding parentheses: mydoubler(10).

########################################################################################

numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)


# The filter() function creates a list of elements for which a function returns True.
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
# 1. 'filter' takes the lambda (the condition) and the list.
# 2. The lambda 'x % 2 != 0' checks if a number is ODD (нечетное).
# 3. If the lambda returns True, the number STAYS.
# 4. If the lambda returns False, the number is REMOVED.
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers) # Output: [1, 3, 5, 7]

# sorted with key 
students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)


