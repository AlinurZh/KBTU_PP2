words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)
# ['pie', 'apple', 'banana', 'cherry']

students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)
# [('Tobias', 22), ('Emil', 25), ('Linus', 28)]

students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)
# [('Tobias', 22), ('Emil', 25), ('Linus', 28)]

people = [
    ("Alice", 30),
    ("Bob", 25),
    ("Charlie", 30),
    ("Diana", 25)
]
sorted_people = sorted(people, key=lambda x: (x[1], x[0]))
print(sorted_people)
# [('Bob', 25), ('Diana', 25), ('Alice', 30), ('Charlie', 30)]