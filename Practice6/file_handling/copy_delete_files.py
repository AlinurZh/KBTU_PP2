import shutil
import os
from pathlib import Path
from datetime import datetime
import glob

print("=" * 50)
print("File operations - copy and delete")
print("=" * 50)

with open("original.txt", "w") as f:
    f.write("This is the original file.\n")
    f.write("It contains important data.\n")
    f.write("Line 3\n")
    f.write("Line 4\n")

print("created original.txt")

with open("data.txt", "w") as f:
    f.write("Sample data file\n")
    f.write("For testing purposes\n")

print("created data.txt")

with open("numbers.txt", "w") as f:
    for i in range(1, 11):
        f.write(f"Number: {i}\n")

print("created numbers.txt")


print("\n--- copying ---")

shutil.copy("original.txt", "copy1.txt")
print("copied original.txt to copy1.txt")

with open("copy1.txt", "r") as f:
    print("content of copy1.txt:")
    print(f.read())

shutil.copy2("original.txt", "copy2.txt")
print("copied with metadata to copy2.txt")

orig_stat = os.stat("original.txt")
c1_stat = os.stat("copy1.txt")
c2_stat = os.stat("copy2.txt")

print(f"\nmodification time:")
print(f"original: {orig_stat.st_mtime}")
print(f"copy1: {c1_stat.st_mtime}")
print(f"copy2: {c2_stat.st_mtime}")


print("\n--- copying to folder ---")

os.makedirs("backup", exist_ok=True)

shutil.copy2("original.txt", "backup/original_backup.txt")
print("copied to backup/")

for fname in ["data.txt", "numbers.txt"]:
    dst = os.path.join("backup", fname)
    shutil.copy2(fname, dst)
    print(f"backup: {fname}")

print("\nin backup folder:")
for item in os.listdir("backup"):
    print(f"  - {item}")


def backup_with_timestamp(filename):
    if not os.path.exists(filename):
        print(f"file {filename} not found")
        return None
    
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name, ext = os.path.splitext(filename)
    new_name = f"{name}_bak_{ts}{ext}"
    
    shutil.copy2(filename, new_name)
    print(f"backup: {new_name}")
    return new_name

backup_with_timestamp("original.txt")
backup_with_timestamp("data.txt")


def safe_copy(src, dst):
    if not os.path.exists(src):
        print(f"error: {src} doesnt exist")
        return False
    
    if os.path.exists(dst):
        print(f"warning: {dst} already exists")
        ans = input("overwrite? (yes/no): ")
        if ans.lower() != "yes":
            print("cancelled")
            return False
    
    shutil.copy2(src, dst)
    print(f"copied {src} -> {dst}")
    return True

safe_copy("original.txt", "safe_copy.txt")
safe_copy("nonexistent.txt", "output.txt")


print("\n--- deleting ---")

with open("temp.txt", "w") as f:
    f.write("temporary\n")

print("created temp.txt")
os.remove("temp.txt")
print("deleted temp.txt")

if not os.path.exists("temp.txt"):
    print("temp.txt is gone")


def safe_del(filename):
    if not os.path.exists(filename):
        print(f"{filename} doesnt exist")
        return False
    
    try:
        os.remove(filename)
        print(f"deleted: {filename}")
        return True
    except PermissionError:
        print(f"no permission to delete {filename}")
        return False
    except Exception as e:
        print(f"error: {e}")
        return False

safe_del("copy1.txt")
safe_del("copy2.txt")
safe_del("random_file.txt")


def del_multiple(files):
    count = 0
    for f in files:
        if safe_del(f):
            count += 1
    print(f"deleted {count} of {len(files)}")

bak_files = glob.glob("*_bak_*.txt")
print(f"\nfound backups: {len(bak_files)}")
for f in bak_files:
    print(f"  {f}")

if bak_files:
    del_multiple(bak_files)


print("\n--- moving ---")

with open("moveme.txt", "w") as f:
    f.write("this file will be moved\n")

os.makedirs("archive", exist_ok=True)

shutil.move("moveme.txt", "archive/moved.txt")
print("moved moveme.txt to archive/")

if not os.path.exists("moveme.txt") and os.path.exists("archive/moved.txt"):
    print("move ok")


print("\n--- renaming ---")

with open("oldname.txt", "w") as f:
    f.write("test\n")

os.rename("oldname.txt", "newname.txt")
print("renamed oldname.txt -> newname.txt")

shutil.move("newname.txt", "finalname.txt")
print("renamed again with move")


print("\n--- batch rename ---")

for i in range(1, 6):
    with open(f"test_{i}.txt", "w") as f:
        f.write(f"test {i}\n")

print("created test_1.txt ... test_5.txt")

for i, fname in enumerate(sorted(glob.glob("test_*.txt")), 1):
    newname = f"file_{i:03d}.txt"
    os.rename(fname, newname)
    print(f"{fname} -> {newname}")


print("\n--- copy entire folder ---")

if os.path.exists("backup"):
    if os.path.exists("backup_copy"):
        shutil.rmtree("backup_copy")
    
    shutil.copytree("backup", "backup_copy")
    print("copied backup/ to backup_copy/")
    
    print("contents of backup_copy/:")
    for item in os.listdir("backup_copy"):
        print(f"  {item}")


def file_info(filename):
    if not os.path.exists(filename):
        print(f"{filename} not found")
        return
    
    st = os.stat(filename)
    size = st.st_size
    
    if size < 1024:
        sz = f"{size} B"
    elif size < 1024*1024:
        sz = f"{size/1024:.1f} KB"
    else:
        sz = f"{size/1024/1024:.1f} MB"
    
    mtime = datetime.fromtimestamp(st.st_mtime)
    
    print(f"\n{filename}")
    print(f"  size: {sz}")
    print(f"  modified: {mtime.strftime('%Y-%m-%d %H:%M')}")
    print(f"  path: {os.path.abspath(filename)}")

file_info("original.txt")
file_info("numbers.txt")


print("\n--- pathlib ---")

p = Path("pathlib_test.txt")
p.write_text("created with pathlib\n")
print(f"created {p.name}")

content = p.read_text()
print(f"content: {content.strip()}")

p2 = Path("pathlib_copy.txt")
p2.write_text(p.read_text())
print(f"copied to {p2.name}")

print(f"exists: {p.exists()}")
print(f"is file: {p.is_file()}")
print(f"size: {p.stat().st_size}")

p2.unlink()
print(f"deleted {p2.name}")


print("\n" + "="*50)
ans = input("delete all test files? (yes/no): ")

if ans.lower() == "yes":
    to_del = ["original.txt", "data.txt", "numbers.txt", 
              "safe_copy.txt", "finalname.txt", "pathlib_test.txt"]
    to_del += glob.glob("file_*.txt")
    
    for f in to_del:
        safe_del(f)
    
    for d in ["backup", "backup_copy", "archive"]:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"deleted folder {d}/")
    
    print("\ndone!")
else:
    print("\nfiles kept")
    print("created files:")
    for item in sorted(os.listdir(".")):
        if item.endswith(".txt") or item in ["backup", "backup_copy", "archive"]:
            typ = "folder" if os.path.isdir(item) else "file"
            print(f"  [{typ}] {item}")