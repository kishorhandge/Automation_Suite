import psutil
import sys
import os
import time
import schedule


# ======================================================
# Scan Processes
# ======================================================
def ProcessScan():

    listprocess = []

    for proc in psutil.process_iter():
        try:
            proc.cpu_percent()
        except:
            pass

    time.sleep(0.2)

    for proc in psutil.process_iter():
        try:

            info = proc.as_dict(attrs=["pid","name","username","status","create_time"])

            try:
                info["create_time"] = time.strftime("%Y-%m-%d %H:%M:%S",
                                    time.localtime(info["create_time"]))
            except:
                info["create_time"] = "NA"

            info["cpu_percent"] = proc.cpu_percent(None)
            info["memory_percent"] = proc.memory_percent()

            listprocess.append(info)

        except (psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
            pass

    return listprocess



# ======================================================
# Create Log File
# ======================================================
def CreateLog(FolderName):

    Border = "-"*50

    os.makedirs(FolderName, exist_ok=True)

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    FileName = os.path.join(FolderName,"Marvellous_%s.log" %timestamp)

    print("Log file created:", FileName, flush=True)

    with open(FileName,"w") as fobj:

        fobj.write(Border+"\n")
        fobj.write("Marvellous Platform Surveillance System\n")
        fobj.write("Log Created At : "+time.ctime()+"\n")
        fobj.write(Border+"\n\n")

        fobj.write("CPU Usage : %s %%\n"%psutil.cpu_percent())
        fobj.write(Border+"\n")

        Mem = psutil.virtual_memory()
        fobj.write("RAM Usage : %s %%\n"%Mem.percent)
        fobj.write(Border+"\n")

        fobj.write("\nDisk Usage\n")
        fobj.write(Border+"\n")

        for part in psutil.disk_partitions():
            try:
                Usage = psutil.disk_usage(part.mountpoint)
                fobj.write("%s -> %s %% used\n"%(part.mountpoint,Usage.percent))
            except:
                pass

        fobj.write(Border+"\n")

        net = psutil.net_io_counters()
        fobj.write("Network Sent : %.2f MB\n"%(net.bytes_sent/(1024*1024)))
        fobj.write("Network Recv : %.2f MB\n"%(net.bytes_recv/(1024*1024)))
        fobj.write(Border+"\n")

        data = ProcessScan()

        for info in data:
            fobj.write("PID : %s\n"%info.get("pid"))
            fobj.write("Name : %s\n"%info.get("name"))
            fobj.write("User : %s\n"%info.get("username"))
            fobj.write("Status : %s\n"%info.get("status"))
            fobj.write("Start : %s\n"%info.get("create_time"))
            fobj.write("CPU %% : %.2f\n"%info.get("cpu_percent"))
            fobj.write("Memory %% : %.2f\n"%info.get("memory_percent"))
            fobj.write(Border+"\n")

    print("System log created successfully", flush=True)



# ======================================================
# Main Function
# ======================================================
def main():

    Border = "-"*50

    print(Border, flush=True)
    print("Marvellous Platform Surveillance System", flush=True)
    print(Border, flush=True)

    if len(sys.argv) == 3:

        interval = int(sys.argv[1])
        folder = sys.argv[2]

        print("Log folder:", folder, flush=True)
        print("Interval:", interval, "minutes", flush=True)

        CreateLog(sys.argv[2])
        schedule.every(int(sys.argv[1])).minutes.do(CreateLog,sys.argv[2])

        print("Surveillance started...", flush=True)

        while True:
            schedule.run_pending()
            time.sleep(1)

    else:

        print("Usage:", flush=True)
        print("python process_surveillance.py <interval_minutes> <folder>", flush=True)



# ======================================================
# Entry Point
# ======================================================
if __name__ == "__main__":
    main()