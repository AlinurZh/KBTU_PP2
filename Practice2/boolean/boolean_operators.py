# Comparison return True or False
a = 10 
b = 20

print(a == b) # False
print(a != b) # True 
print(a < b) # True
print(a > b) # False 
print(a <= 10) # True
print(b >= 15) # True

x = True 
y = False 
print(x and y) # False 
print(x or y) # True 
print(not x) # False 
print(not y) # True

# Most Values are True. Almost any value is evaluated to True if it has some sort of content.

print(bool("abc"))
print(bool(123))
print(bool(["apple", "cherry", "banana"]))

# Some Values are False

print(bool(False))
print(bool(None))
print(bool(0))
print(bool(""))
print(bool(()))
print(bool([]))
print(bool({}))

# isinstance() is a way to check the data type of a variable.
x = 200
print(isinstance(x, int))