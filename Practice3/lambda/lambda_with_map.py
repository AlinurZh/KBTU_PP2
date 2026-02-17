numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)

names = ['Alice', 'Bob', 'Charlie', 'David']
first_letters = list(map(lambda name: name[0], names))
print(first_letters)  # ['A', 'B', 'C', 'D']

numbers1 = [1, 2, 3, 4]
numbers2 = [10, 20, 30, 40]
result = list(map(lambda x, y: x + y, numbers1, numbers2))
print(result)  # [11, 22, 33, 44]

a = [1, 2, 3]
b = [10, 20, 30]
c = [100, 200, 300]
result = list(map(lambda x, y, z: x + y + z, a, b, c))
print(result)  # [111, 222, 333]

short = [1, 2, 3]
long = [10, 20, 30, 40, 50]
result = list(map(lambda x, y: x + y, short, long))
print(result)  # [11, 22, 33]

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = list(map(lambda x: x * 2 if x % 2 == 0 else x * 3, numbers))
print(result)  # [3, 4, 9, 8, 15, 12, 21, 16, 27, 20]
