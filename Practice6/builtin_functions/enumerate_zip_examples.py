fruits = ["apple", "banana", "cherry", "date"]
print("=== Without enumerate ===")
for i in range(len(fruits)):
    print(f"    {i}:  {fruits[i]}")

print("\n=== With enumerate ===")
for i, fruit in enumerate(fruits):
    print(f"    {i}:  {fruit}")

print("\n=== With enumerate startind from 1 ===")
for i, fruit in enumerate(fruit, start=1):
    print(f"    {i}.  {fruit}")

names = ["Alinur", "Alice", "Bob", "Dima"]
scores = [98, 76, 86, 70]
grades = ["A+" ,"B+", "A", "B"]

print("\n=== zip() two lists ===")
for name, score in zip(names, scores):
    print(f"    {name}: {score}")

print("\n=== zip() three lists ===")
for name, score, grade in zip(names, scores, grades):
    print(f"  {name}: {score} ({grade})")

numbers = [1, 2, 3, 4, 5]
letters = ["a", "b", "c"]
print("\n=== zip() stops at shortest ===")
print(numbers)
print(letters)
for num, letter in zip(numbers, letters):
    print(f"    {num} - {letter}")

values = [42, 3.14, "hello", True, [1, 2, 3], {"key": "value"}]
print("\n=== type() checking ===")
for v in values:
    print(f"  {str(v):<20} -> type: {type(v).__name__}")

print("\n=== isinstance() checking ===")
x = 42
print(f"  is int?   {isinstance(x, int)}")
print(f"  is float? {isinstance(x, float)}")
print(f"  is str?   {isinstance(x, str)}")

print("\n=== Type conversions ===")

print(f"  int('42')     = {int('42')}")
print(f"  int(3.99)     = {int(3.99)}")      # truncates decimal
print(f"  int(True)     = {int(True)}")

print(f"  float('3.14') = {float('3.14')}")
print(f"  float(42)     = {float(42)}")

print(f"  str(42)       = '{str(42)}'")
print(f"  str(3.14)     = '{str(3.14)}'")
print(f"  str(True)     = '{str(True)}'")

print(f"  bool(0)       = {bool(0)}")
print(f"  bool(1)       = {bool(1)}")
print(f"  bool('')      = {bool('')}")
print(f"  bool('hello') = {bool('hello')}")

text = "hello"
print(f"\n  list('hello')  = {list(text)}")
print(f"  tuple([1,2,3]) = {tuple([1, 2, 3])}")
print(f"  set([1,1,2,3]) = {set([1, 1, 2, 3])}")
