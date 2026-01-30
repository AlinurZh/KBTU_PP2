# Basic comparison operations
print(10 > 9)
print(10 == 9)
print(10 < 9)

# Using isinstance to check the data type
x = 200
print(isinstance(x, int))

# ADDED: Inequality operator
print(5 != "5") # True, because an integer is not equal to a string

# ADDED: Comparing lists (Checks if content is identical)
list_a = [1, 2]
list_b = [1, 2]
print(list_a == list_b) # True