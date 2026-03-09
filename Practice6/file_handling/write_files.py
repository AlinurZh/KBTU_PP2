import os 
print("=" * 50)
print("MODE 'w' - Write (overwrites if file exists)")
print("=" * 50)

with open("sample.txt", "w") as f:
    f.write("Hello, World!\n")
    f.write("This is a sample file.\n")
    f.write("Python is an amazing programming language.\n")

print("File 'sample.txt' created and written successfully!")

with open("sample.txt", "r") as f:
    print("\nContent of 'sample.txt':")
    print(f.read())

print("=" * 50)
print("MODE 'w' - Overwrites existing content")
print("=" * 50)

with open("sample.txt", "w") as f:
    f.write("NEW CONTENT - old content is gone!\n")

print("File overwritten!")

with open("sample.txt", "r") as f:
    print("\nNew content:")
    print(f.read())

print("=" * 50)
print("MODE 'a' - Append (adds to existing content)")
print("=" * 50)

with open("sample.txt", "a") as f:
    f.write("This line was appended.\n")
    f.write("And this one too.\n")

print("Content appended to 'sample.txt'!")

with open("sample.txt", "r") as f:
    print("\nContent after append:")
    print(f.read())

print("=" * 50)
print("MODE 'x' - Exclusive creation (error if exists)")
print("=" * 50)

if not os.path.exists("new_file.txt"):
    with open("new_file.txt", "x") as f:
        f.write("This file was created with mode 'x'\n")
    print("File 'new_file.txt' created successfully!")
else:
    print("File 'new_file.txt' already exists.")

#(will fail)
try:
    with open("new_file.txt", "x") as f:
        f.write("This will not work!\n")
except FileExistsError:
    print("Error: File already exists! Cannot use 'x' mode.")

print("=" * 50)
print("Using writelines() - Write multiple lines")
print("=" * 50)

lines = [
    "First line\n",
    "Second line\n",
    "Third line\n",
    "Fourth line\n"
]

with open("multiline.txt", "w") as f:
    f.writelines(lines) # Allows us to write several lines

print("File 'multiline.txt' created with writelines()!")

with open("multiline.txt", "r") as f:
    print("\nContent:")
    print(f.read())

print("=" * 50)
print("Writing without explicit newlines")
print("=" * 50)

with open("no_newlines.txt", "w") as f:
    f.write("Line 1")
    f.write("Line 2")  
    f.write("Line 3")

with open("no_newlines.txt", "r") as f:
    print("Content without \\n:")
    print(f.read())

with open("with_newlines.txt", "w") as f:
    f.write("Line 1\n")
    f.write("Line 2\n")
    f.write("Line 3\n")

with open("with_newlines.txt", "r") as f:
    print("\nContent with \\n:")
    print(f.read())

print("\n" + "=" * 50)
print("Using print() to write to file")
print("=" * 50)

with open("print_output.txt", "w") as f:
    print("Hello from print()", file=f)
    print("This is line 2", file=f)
    print("Python version", 3.11, file=f)

with open("print_output.txt", "r") as f:
    print("Content written by print():")
    print(f.read())


