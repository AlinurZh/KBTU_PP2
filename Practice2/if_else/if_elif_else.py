# The elif keyword (short for else if)
a = 33
b = 33
if b > a:
    print("b is greater than a")
elif a == b:
    print("a and b are equal")
else:
    print("a is greater than b")

# Multiple elif conditions: Grading system
score = 75
if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
elif score >= 60:
    print("Grade: D")

# Testing logical operators: AND
a, b, c = 200, 33, 500
if a > b and c > a:
    print("Both conditions are True")

# Testing logical operators: OR
if a > b or a > c:
    print("At least one condition is True")

# Testing logical operators: NOT
if not a > b:
    print("a is NOT greater than b")

# --- NESTED IF STATEMENTS ---
x = 41
if x > 10:
    print("Above ten,")
    if x > 20:
        print("and also above 20!")
    else:
        print("but not above 20.")

# Complex nesting for login validation
username, password, is_active = "Emil", "python123", True
if username:
    if password:
        if is_active:
            print("Login successful")
        else:
            print("Account is not active")