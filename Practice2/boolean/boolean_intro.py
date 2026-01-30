# Basic use of the bool() function
print(bool("Hello"))
print(bool(15))

# Evaluating variables
x = "Hello"
y = 15
print(bool(x))
print(bool(y))

# Values that evaluate to True
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

# Values that evaluate to False (Crucial to remember!)
print(bool(False))
print(bool(None))
print(bool(0))
print(bool(""))
print(bool(()))
print(bool([]))
print(bool({}))

# Example with a class object that returns 0 in __len__
class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj))

# ADDED: Testing for an empty string (Common real-world practice)
username = ""
if not username:
    print("Username is empty!")