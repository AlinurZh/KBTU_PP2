# Basic If statement
a = 33
b = 200
if b > a:
    print("b is greater than a")

# Checking if a number is positive
number = 15
if number > 0:
    print("The number is positive")

# Using a boolean variable directly
is_logged_in = True
if is_logged_in:
    print("Welcome back!")

# Multiple statements in one if block
age = 20
if age >= 18:
    print("You are an adult")
    print("You can vote")
    print("You have full legal rights")

# The 'pass' statement: Used as a placeholder to avoid errors in empty blocks
a = 33
b = 200
if b > a:
    pass 

# Placeholder for future implementation
age = 16
if age < 18:
    pass  # TODO: Add underage logic later
else:
    print("Access granted")

# INFO: If statement without indentation will raise an IndentationError
# if b > a:
# print("b is greater than a")