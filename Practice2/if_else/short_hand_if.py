# One-line if statement
a = 5
b = 2
if a > b: print("a is greater than b")

# One-line if/else (Ternary Operator)
a = 2
b = 330
print("A") if a > b else print("B")

# Assigning a value using short-hand
x, y = 15, 20
max_value = x if x > y else y
print("Maximum value:", max_value)

# Setting a default value
username = ""
display_name = username if username else "Guest"
print("Welcome,", display_name)

# One line, three outcomes (Nested Ternary)
a, b = 330, 330
print("A") if a > b else print("=") if a == b else print("B")