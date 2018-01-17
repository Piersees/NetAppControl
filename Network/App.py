import psutil

for proc in psutil.process_iter():
    process = psutil.Process(proc.pid)
    pname = process.name()
    print("Name: ", pname, "    pid: ",process.pid)
