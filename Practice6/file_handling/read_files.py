print("=" * 50)
print("METHOD 1: read() - Read entire file")
print("=" * 50)

with open("sample.txt", "r") as f:
    content = f.read()
    print(content)
  
print('\n' + '=' * 50)
print("METHOD 2: readline() - Read line by line")
print("=" * 50)

with open("sample.txt", "r") as f:
    line1 = f.readline() #line1 = "SOMETHING\n"
    line2 = f.readline()
    print(f"First line: {line1.strip()}")
    print(f"Second line: {line2.strip()}")

print('\n' + "=" * 50)
print("METHOD 3: readlines() - Read all lines as list")
print("=" * 50)

with open("sample.txt", "r") as f:
    lines = f.readlines()
    for i, line in enumerate(lines, 1):
        print(f"Line {i}: {line.strip()}")

print("\n" + "=" * 50)
print("METHOD 4: Iterate over file directly")
print("=" * 50)

with open("sample.txt", "r") as f:
    # The file object f is an iterable
    for line in f:
        print(f">> {line.strip()}")

print('\n' + "=" * 50)
print("METHOD 5: Reading partial content - read(n)")
print("=" * 50)

with open("sample.txt", "r") as f:
    chunk = f.read(20)
    print(f"First 20 characters: '{chunk}'")

print('\n' + "=" * 50)
print("METHOD 6: Reading with error handling")
print("=" * 50)

try:
    with open("sample.txt", "r") as f:
        content = f.read()
        print("File content:")
        print(content)
except FileNotFoundError:
    print("Error: File not found!")
except PermissionError:
    print("Error: Permission denied!")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 50)
print("METHOD 7: Without 'with' statement (old way)")
print("=" * 50)

f = open("sample.txt", "r")
content = f.read()
print(content)
f.close()  # Must manually close!
print("File closed manually.")

print("\n" + "=" * 50)
print("Checking if file is closed")
print("=" * 50)

with open("sample.txt", "r") as f:
    # attribute (property) of the file object
    print(f"Inside 'with' block: File closed? {f.closed}")
print(f"After 'with' block: File closed? {f.closed}")

print("\n" + "=" * 50)
print("METHOD 8: Reading large files efficiently")
print("=" * 50)

line_count = 0
word_count = 0
char_count = 0
with open("sample.txt", "r") as f:
    for line in f:
        line_count += 1
        word_count += len(line.split())
        char_count += len(line)

print(f"Total lines: {line_count}")
print(f"Total words: {word_count}")
print(f"Total characters: {char_count}")

print("\n" + "=" * 50)
print("METHOD 9: Reading specific lines")
print("=" * 50)

with open("sample.txt", "r") as f:
    lines = f.readlines()
    if len(lines) >= 3:
        print(f"Third line: {lines[2].strip()}")
    else:
        print("File has less than 3 lines")

# --- Reading file backwards ---
print("\n" + "=" * 50)
print("METHOD 10: Reading file backwards")
print("=" * 50)

with open("sample.txt", "r") as f:
    lines = f.readlines()
    for line in reversed(lines):
        print(f"<< {line.strip()}")