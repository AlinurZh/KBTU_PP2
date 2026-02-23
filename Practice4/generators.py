#1:
def SquareGenerator(n):
    for i in range(n + 1):
        yield i ** 2
n = int(input())
print(*SquareGenerator(n))

#2:
def EvenGenerator(m):
    for i in range(0, m + 1):
        if i % 2 == 0:
            yield i
m = int(input())
print(*EvenGenerator(m), sep=", ")

#3:
def IterGenerator(k):
    for i in range(k + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
k = int(input())
print(*IterGenerator(k))

#4:
def Squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

a, b = map(int, input().split())
print(*Squares(a, b))

#5:
def DownGenerator(d):
    for i in range(d, -1, -1):
        yield i
d = int(input())
print(*DownGenerator(d))

