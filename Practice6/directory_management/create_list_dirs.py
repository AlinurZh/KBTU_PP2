import os
from pathlib import Path
import shutil

# -----------------------------
# Create nested directories
# -----------------------------

Path("myProject").mkdir(exist_ok=True)
print("[mkdir] Created 'myProject/'")
Path("myProject/src/utilits").mkdir( parents=True, exist_ok=True)
Path("myProject/src/models").mkdir(parents=True, exist_ok=True)
Path("myProject/tests").mkdir(parents=True, exist_ok=True)
Path("myProject/data/raw").mkdir(parents=True, exist_ok=True)
Path("myProject/data/processed").mkdir(parents=True, exist_ok=True)
print("[mkdir] Created nested folder structure inside 'myProject/'")

Path("myProject/src/main.py").write_text("# main entry point\n")
Path("myProject/src/utilits/helpers.py").write_text("# helper functions\n")
Path("myProject/src/utilits/validators.py").write_text("# validators\n")
Path("myProject/src/models/user.py").write_text("# User model")
Path("myProject/tests/testMain.py").write_text("# tests\n")
Path("myProject/data/raw/data.csv").write_text("id,name\n1,Alice\n2,Bob\n")
Path("myProject/data/processed/clean.csv").write_text("id,name\n1,Alice\n2,Bob\n")
Path("myProject/README.md").write_text("# My Project\n")
Path("myProject/config.json").write_text('{"debug": true}\n')
print("[setup] Sample files created\n")

print("=== os.listdir() -> top level of my 'myProfect/' ===")
for item in os.listdir("myProject"):
    print(f"    {item}")

print("=== os.wolk() -> full directory tree ===")
for root, dirs, files in os.walk("myProject"):
    level = root.replace("myProject", "").count(os.sep)
    indent = "    " * level
    print(f"{indent}{os.path.basename(root)}/")
    for file in files:
        print(f"{indent}    {file}")

print("\n=== pathlib iterdir() -> top level ===")
for item in Path("myProject").iterdir():
    kind = "DIR " if item.is_dir() else "FILE"
    print(f"  [{kind}] {item.name}")

print("\n=== Find all .py files ===")
for i in Path("myProject").rglob("*.py"):
    print(f"    {i}")

print("\n=== Find all .csv files ===")
for i in Path("myProject").rglob("*.csv"):
    print(f"    {i}")

print("\n=== Find all .md files ===")
for i in Path("myProject").rglob("*.md"):
    print(f"    {i}")

from collections import Counter
extensions = Counter(i.suffix for i in Path("myProject").rglob("*") if i.is_file())
print("\n=== File count by extension ===")
for ext, count in extensions.items():
    print(f"    {ext}: {count} file(s)")

shutil.rmtree("myProject")
print("\n[cleanup] Removed 'myProject/'")