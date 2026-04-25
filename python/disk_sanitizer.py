import hashlib
import os
import time
import schedule
import sys


# ======================================================
# Generate file hash
# ======================================================
def CalculateCheckSum(FileName):

    hobj = hashlib.md5()

    try:
        with open(FileName,"rb") as fobj:

            Buffer = fobj.read(1000)

            while len(Buffer) > 0:
                hobj.update(Buffer)
                Buffer = fobj.read(1000)

    except:
        return None

    return hobj.hexdigest()



# ======================================================
# Find duplicate files
# ======================================================
def FindDuplicate(DirectoryName):

    Border = "-"*50

    FolderName = "Logs"

    if not os.path.exists(FolderName):
        os.mkdir(FolderName)
        print("Log folder created", flush=True)

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

    LogFile = os.path.join(FolderName,"Smart_%s.log" % timestamp)

    print("Log file created:",LogFile, flush=True)

    fobj = open(LogFile,"w")

    fobj.write(Border+"\n")
    fobj.write("SMART DIRECTORY AUTOMATION LOG\n")
    fobj.write(Border+"\n")
    fobj.write("Start Time : "+time.ctime()+"\n")
    fobj.write("Directory  : "+DirectoryName+"\n\n")

    if not os.path.exists(DirectoryName):

        print("Directory not found", flush=True)
        fobj.write("Directory not found\n")
        fobj.close()
        return None, None


    Duplicate = {}
    TotalFiles = 0

    for FolderName,SubFolderName,FileNames in os.walk(DirectoryName):

        for Fname in FileNames:

            TotalFiles += 1

            Path = os.path.join(FolderName,Fname)

            CheckSum = CalculateCheckSum(Path)

            if CheckSum is None:
                continue

            if CheckSum in Duplicate:
                Duplicate[CheckSum].append(Path)
            else:
                Duplicate[CheckSum] = [Path]


    fobj.write("Total Files Scanned : "+str(TotalFiles)+"\n\n")

    fobj.write(Border+"\n")
    fobj.write("Duplicate Files Found\n")
    fobj.write(Border+"\n")

    for value in Duplicate.values():

        if len(value) > 1:

            for file in value:
                fobj.write(file+"\n")

            fobj.write("\n")

    fobj.close()

    return Duplicate, LogFile



# ======================================================
# Delete duplicate files
# ======================================================
def DeleteDuplicate(path):

    MyDict, LogFile = FindDuplicate(path)

    if MyDict is None:
        return

    Result = list(filter(lambda x : len(x) > 1 ,MyDict.values()))

    fobj = open(LogFile,"a")

    fobj.write("\n"+"-"*50+"\n")
    fobj.write("Deleted Files\n")
    fobj.write("-"*50+"\n")

    Count = 0
    Deleted = 0

    for value in Result:

        for subvalue in value:

            Count += 1

            if Count > 1:

                try:
                    os.remove(subvalue)

                    print("Deleted:",subvalue, flush=True)

                    fobj.write(subvalue+"\n")

                    Deleted += 1

                except Exception as e:

                    print("Cannot delete:",subvalue, flush=True)

        Count = 0

    fobj.write("\nTotal Deleted Files : "+str(Deleted)+"\n")
    fobj.write("End Time : "+time.ctime()+"\n")
    fobj.write("-"*50+"\n")

    fobj.close()

    print("Total deleted files:",Deleted, flush=True)



# ======================================================
# Main
# ======================================================
def main():

    Border = "-"*50

    print(Border, flush=True)
    print("Smart Directory Automation", flush=True)
    print(Border, flush=True)

    if len(sys.argv) == 2:

        path = sys.argv[1]

        print("Directory:",path, flush=True)

        DeleteDuplicate(sys.argv[1])
        schedule.every(1).minutes.do(DeleteDuplicate,sys.argv[1])

        print("Automation started", flush=True)
        print("Logs stored in Logs folder", flush=True)
        print("Press Ctrl+C to stop", flush=True)

        while True:

            schedule.run_pending()
            time.sleep(1)

    else:

        print("Usage:", flush=True)
        print("python disk_sanitizer.py <directory>", flush=True)



# ======================================================
# Entry point
# ======================================================
if __name__ == "__main__":
    main()