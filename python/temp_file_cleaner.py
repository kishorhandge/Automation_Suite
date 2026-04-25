import os
import sys


if len(sys.argv) < 2:
    print("Error: Directory path not provided", flush=True)
    sys.exit()

path = sys.argv[1]


if not os.path.exists(path):
    print("Error: Folder does not exist", flush=True)
    sys.exit()

print("Scanning folder:", path, flush=True)

deleted_count = 0

for root, dirs, files in os.walk(path):

    for file in files:

        if file.endswith(".tmp") or file.endswith(".log"):

            file_path = os.path.join(root, file)

            try:
                os.remove(file_path)
                print("Deleted:", file_path, flush=True)
                deleted_count += 1
            except Exception as e:
                print("Error deleting:", file_path, "-", str(e), flush=True)

print("Total files deleted:", deleted_count, flush=True)