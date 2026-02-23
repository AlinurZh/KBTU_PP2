import math

#1: Degree to Radian
print("=== Degree to Radian ===")
degree = float(input("Input degree: "))
radian = math.radians(degree)
print(f"Output radian: {radian:.6f}")

print()

#2: Area of Trapezoid
print("=== Area of Trapezoid ===")
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))
area_trapezoid = 0.5 * (base1 + base2) * height
print(f"Expected Output: {area_trapezoid}")

print()

#3: Area of Regular Polygon
print("=== Area of Regular Polygon ===")
sides = int(input("Input number of sides: "))
length = float(input("Input the length of a side: "))
area_polygon = (sides * length ** 2) / (4 * math.tan(math.pi / sides))
print(f"The area of the polygon is: {area_polygon:.0f}")

print()

#4: Area of Parallelogram
print("=== Area of Parallelogram ===")
base = float(input("Length of base: "))
height_para = float(input("Height of parallelogram: "))
area_parallelogram = base * height_para
print(f"Expected Output: {area_parallelogram}")