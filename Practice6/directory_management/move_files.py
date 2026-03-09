import os
import shutil
from pathlib import Path

for folder in ["inbox", "archive", "backup", "images", "docs"]:
    Path(folder).mkdir(exist_ok=True)

Path("inbox/report.txt").write_text("Q1 financial report.")
Path("inbox/notes.txt").write_text("Meeting notes")
Path("inbox/summary.txt").write_text("Project summary")
Path("inbox/photo.png").write_text("Imange placeholder")
Path("inbox/diagram.png").write_text("Diagram placeholder")
print("[setup] Created sample files in 'inbox/'")

shutil.move("inbox/report.txt", "archive/report.txt")
print("[move] 'inbox/report.txt' -> 'archive/report.txt'")

src = Path("inbox/summary.txt")
dst = Path("docs/summary.txt")
shutil.move(str(src), str(dst))
print(f"[move] '{src}' -> '{dst}'")

shutil.copy("inbox/notes.txt", "archive/notes.txt")
print("[copy] 'inbox/notes.txt' → 'archive/notes.txt'")

print("\n[copy] Moving all .png files ->'images/'")
for png in Path("inbox").glob("*.png"):
    shutil.copy(png, Path("images") / png.name)
    print(f"    copied '{png.name}'")

if Path("backup/archive").exists():
    shutil.rmtree("backup/archive")

shutil.copytree("archive", "backup/archive")
print("\n[copytree] Copied entire 'archive/' -> 'backup/archive/'")

print("\n=== Final folder contents ===")
for folder in ["inbox", "archive", "docs", "images", "backup/archive"]:
    files = list(Path(folder).iterdir())
    names = [i.name for i in files] if files else ["(empty)"]
    print(f"  {folder}/: {', '.join(names)}")

for folder in ["inbox", "archive", "backup", "images", "docs"]:
    shutil.rmtree(folder, ignore_errors=True)
print("\n[cleanup] All demo folders removed.")