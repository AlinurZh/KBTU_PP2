# The elif keyword is Python's way of saying "if the previous conditions were not true, then try this condition.
a = 33
b = 33
if b > a:
  print("b is greater than a")
elif a == b:
    print("a and b are equal")

# Other example

day = 3

if day == 1:
  print("Monday")
elif day == 2:
  print("Tuesday")
elif day == 3:
  print("Wednesday")
elif day == 4:
  print("Thursday")
elif day == 5:
  print("Friday")
elif day == 6:
  print("Saturday")
elif day == 7:
  print("Sunday")

# if + elif + else 

number = 7

if number % 2 == 0:
  print("The number is even")
else:
  print("The number is odd")
