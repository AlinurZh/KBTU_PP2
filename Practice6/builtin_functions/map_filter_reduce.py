from functools import reduce

numbers = [1, 2, 3, 4, 5]

squared = list(map(lambda x: x ** 2, numbers))
print(f"Original:   {numbers}")
print(f"Squared:    {squared}")

words = ["hello", "world", "python"]
uppercased = list(map(str.upper, words))
print(f"\nOriginal:     {words}")
print(f"Uppercased:     {uppercased}")

str_numbers = ["1", "2", "3", "4", "5"]
integers = list(map(int, str_numbers))
print(f"\nStrings:  {str_numbers}")
print(f"Integers:   {integers}")

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"\nOriginal:  {numbers}")
print(f"Evens:   {evens}")

greater = list(filter(lambda x: x > 5, numbers))
print(f"Greater than 5:   {greater}")

strings = ["apple", "", "banana", "/", "", "Alinur"]
none_empty = list(filter(None, strings))
print(f"\nWith empty:    {strings}")
print(f"Without empty:  {none_empty}")

numbers = [1, 2, 3, 4, 5]
total = reduce(lambda x, y: x + y, numbers)
print(f"\nNumbers:  {numbers}")
print(f"Sum with reduce():  {total}")

product = reduce(lambda x, y: x * y, numbers)
print(f"Product with reduce():  {product}")

maximum = reduce(lambda x, y: x if x > y else y, numbers)
print(f"Maximum with reduce(): {maximum}")

words = ["Python", "is", "awesome"]
sentence = reduce(lambda x, y: x + " " + y, words)
print(f"\nWords:    {words}")
print(f"Sentence: {sentence}")