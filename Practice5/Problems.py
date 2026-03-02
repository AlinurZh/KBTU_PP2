import re


def task1_a_followed_by_zero_or_more_b(text):
    pattern = r'ab*'
    match = re.search(pattern, text)
    return match.group() if match else None


def task2_a_followed_by_two_three_b(text):
    pattern = r'ab{2,3}'
    match = re.search(pattern, text)
    return match.group() if match else None


def task3_lowercase_with_underscore(text):
    pattern = r'[a-z]+_[a-z]+'
    matches = re.findall(pattern, text)
    return matches if matches else None


def task4_uppercase_followed_by_lowercase(text):
    pattern = r'[A-Z][a-z]+'
    matches = re.findall(pattern, text)
    return matches if matches else None


def task5_a_followed_by_anything_ending_b(text):
    pattern = r'a.*b'
    match = re.search(pattern, text)
    return match.group() if match else None


def task6_replace_with_colon(text):
    pattern = r'[ ,.]'
    result = re.sub(pattern, ':', text)
    return result


def task7_snake_to_camel(text):
    pattern = r'_([a-z])'
    result = re.sub(pattern, lambda m: m.group(1).upper(), text)
    return result


def task8_split_at_uppercase(text):
    pattern = r'[A-Z]'
    result = re.split(pattern, text)
    return result


def task9_insert_spaces(text):
    pattern = r'([A-Z])'
    result = re.sub(pattern, r' \1', text).strip()
    return result


def task10_camel_to_snake(text):
    pattern = r'([A-Z])'
    result = re.sub(pattern, r'_\1', text).lower().lstrip('_')
    return result


print("=" * 70)
print("PYTHON REGEX EXERCISES")
print("=" * 70)

print("\n Task 1: 'a' followed by zero or more 'b's")
print("-" * 50)
for test in ["a", "ab", "abbb", "hello", "cab"]:
    print(f"  '{test}' → {task1_a_followed_by_zero_or_more_b(test)}")

print("\n Task 2: 'a' followed by two to three 'b's")
print("-" * 50)
for test in ["a", "ab", "abb", "abbb", "abbbb"]:
    print(f"  '{test}' → {task2_a_followed_by_two_three_b(test)}")

print("\n Task 3: Lowercase letters joined with underscore")
print("-" * 50)
for test in ["hello_world", "foo_bar_baz", "Hello_World", "test"]:
    print(f"  '{test}' → {task3_lowercase_with_underscore(test)}")

print("\n Task 4: Uppercase followed by lowercase letters")
print("-" * 50)
for test in ["HelloWorld", "HELLO", "hello", "PyThOn"]:
    print(f"  '{test}' → {task4_uppercase_followed_by_lowercase(test)}")

print("\n Task 5: 'a' followed by anything, ending in 'b'")
print("-" * 50)
for test in ["ab", "axxxb", "a123b", "acccccb", "abc"]:
    print(f"  '{test}' → {task5_a_followed_by_anything_ending_b(test)}")

print("\n Task 6: Replace space, comma, or dot with colon")
print("-" * 50)
for test in ["hello world", "a,b,c", "one.two.three", "a b,c.d"]:
    print(f"  '{test}' → '{task6_replace_with_colon(test)}'")

print("\n Task 7: Convert snake_case to camelCase")
print("-" * 50)
for test in ["hello_world", "my_variable_name", "snake_case"]:
    print(f"  '{test}' → '{task7_snake_to_camel(test)}'")

print("\n Task 8: Split string at uppercase letters")
print("-" * 50)
for test in ["HelloWorld", "SplitAtUpperCase", "ABC"]:
    print(f"  '{test}' → {task8_split_at_uppercase(test)}")

print("\n Task 9: Insert spaces between capital letters")
print("-" * 50)
for test in ["HelloWorld", "InsertSpacesHere", "MyVariableName"]:
    print(f"  '{test}' → '{task9_insert_spaces(test)}'")

print("\n Task 10: Convert camelCase to snake_case")
print("-" * 50)
for test in ["camelCase", "HelloWorld", "myVariableName"]:
    print(f"  '{test}' → '{task10_camel_to_snake(test)}'")

print("\n" + "=" * 70)
print("ALL TASKS COMPLETED!")
print("=" * 70)