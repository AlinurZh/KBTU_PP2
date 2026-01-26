# Boolean_comparison.py
# Boolean values in comparison
a = 200
b = 33

if b > a:
  print("b is greater than a")
else:
  print("b is not greater than a")

# Functions can return a boolean 
def myFunction(n):
    if n >= 9 and n <= 12:
        return True
    else:
        return False

n = int(input("Enter a number: "))

if myFunction(n):
    print("YES!")
else:
    print("NO!")




