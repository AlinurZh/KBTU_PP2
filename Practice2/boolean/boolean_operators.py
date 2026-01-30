# Print a message based on whether the condition is True or False
a = 200
b = 33

if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

# Print the answer of a function
def myFunction() :
  return True

print(myFunction())

# Print "YES!" if the function returns True, otherwise print "NO!"
if myFunction():
  print("YES!")
else:
  print("NO!")

# ADDED: Combining conditions with 'and' / 'or'
age = 20
has_ticket = True
if age >= 18 and has_ticket:
    print("Entry allowed")