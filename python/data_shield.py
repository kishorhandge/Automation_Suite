import sys
import os
import time
import schedule
import shutil
import hashlib
import zipfile


# ======================================================
# Create Zip Archive
# ======================================================
def Make_Zip(folder):

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    zip_name = folder + "_" + timestamp + ".zip"

    zobj = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(folder):
        for file in files:

            full_path = os.path.join(root, file)
            relative = os.path.relpath(full_path, folder)

            zobj.write(full_path, relative)

    zobj.close()

    return zip_name


# ======================================================
# Generate File Hash
# ======================================================
def Calculate_hash(path):

    hobj = hashlib.md5()

    with open(path, "rb") as fobj:

        while True:
            data = fobj.read(1024)

            if not data:
                break

            hobj.update(data)

    return hobj.hexdigest()


# ======================================================
# Backup Files
# ======================================================
def BackUpFiles(Source, Destination):

    Copied_Files = []

    print("Creating backup folder...", flush=True)

    os.makedirs(Destination, exist_ok=True)

    for root, dirs, files in os.walk(Source):

        for file in files:

            src_path = os.path.join(root, file)
            relative = os.path.relpath(src_path, Source)
            dest_path = os.path.join(Destination, relative)

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            if (not os.path.exists(dest_path)) or (Calculate_hash(src_path) != Calculate_hash(dest_path)):

                shutil.copy2(src_path, dest_path)

                Copied_Files.append(relative)

                print("Copied:", relative, flush=True)

    return Copied_Files


# ======================================================
# Backup Process
# ======================================================
def MarvellousDataShieldStart(Source="Data"):

    Border = "-" * 50
    BackupName = "MarvellousBackup"

    print(Border, flush=True)
    print("Backup Process Started:", time.ctime(), flush=True)
    print(Border, flush=True)

    files = BackUpFiles(Source, BackupName)

    zip_file = Make_Zip(BackupName)

    print(Border, flush=True)
    print("Backup Completed Successfully", flush=True)
    print("Files Copied:", len(files), flush=True)
    print("Zip File Created:", zip_file, flush=True)
    print(Border, flush=True)


# ======================================================
# Main Function
# ======================================================
def main():

    Border = "-" * 50

    print(Border, flush=True)
    print("Marvellous Data Shield System", flush=True)
    print(Border, flush=True)

    if len(sys.argv) == 3:

        interval = int(sys.argv[1])
        source = sys.argv[2]

        print("Backup Interval:", interval, "seconds", flush=True)
        print("Source Directory:", source, flush=True)

        MarvellousDataShieldStart(sys.argv[2])
        schedule.every(int(sys.argv[1])).seconds.do(MarvellousDataShieldStart,sys.argv[2])

        print(Border, flush=True)
        print("Backup Scheduler Started", flush=True)
        print("Press Ctrl+C to stop", flush=True)
        print(Border, flush=True)

        while True:

            schedule.run_pending()
            time.sleep(1)

    else:

        print("Usage:", flush=True)
        print("python data_shield.py <interval_seconds> <source_folder>", flush=True)


# ======================================================
# Entry Point
# ======================================================
if __name__ == "__main__":
    main()