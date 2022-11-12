import math, time, subprocess, hashlib, platform
import multiprocessing as mp
import threading as thr

# TODO: Multithread this, give ability to add files while running
# TODO: Add ability to remove files from tracking

DEBUG_PRINT = True
PLATFORM = ""

def checkPlatform():
    global PLATFORM
    if platform.system == "Windows":
        PLATFORM = "Windows"
    elif platform.system == "Darwin" or platform.system == "Linux":
        PLATFORM = "Unix"
    else:
        print("Unsupported platform")
        exit()

def debug_print(*args: str)-> None:
    if DEBUG_PRINT:
        print(*args)

def windowsFileCheck(fl: str) -> bool:
    try:
        subprocess.run(["type", fl], check=True)
        return True
    except:
        return False

def unixFileCheck(fl: str) -> bool:
    try:
        subprocess.check_output(f"cat {fl} > /dev/null", shell=True)
        return True
    except:
        return False

def fileExists(fl: str) -> bool:
    if PLATFORM == "Windows":
        exists = windowsFileCheck(fl)
    elif PLATFORM == "Unix":
        exists = unixFileCheck(fl)
            
    if not exists:
        debug_print(f"File {fl} does not exist, please try again")
        return False
        
    return True

def inputFiles(trackedFiles: list[str])-> None:
    while True:
        addFile()
        
        done = input("Press enter to continue, or type 'done' to finish: ")
        if done.lower() == "done":
            debug_print(f"Files to be saved: {trackedFiles}")
            break

def addFile(trackedFiles: list[str], pipe: mp.Pipe) -> None:
    fl = input("File to be added to tracking: ")
    if not fileExists(fl):
        return
        
    trackedFiles.append(fl)
    pipe.send(f"track {fl}")

def removeFile(trackedFiles: list[str], pipe: mp.Pipe) -> None:
    fl = input("File to be removed from tracking: ")
    if not fl in trackedFiles:
        print(f"File {fl} is not being tracked, please try again")
        return
        
    trackedFiles.remove(str(fl))
    pipe.send(f"untrack {fl}")

def hashFile(fl: str) -> str:
    with open(fl, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def hashFiles(trackedFiles: list[str], hashes: dict[str, str]) -> None:
    for fl in trackedFiles:
        debug_print(f"Hashing {fl}")
        hashes[fl] = hashFile(fl)

def collectFiles(trackedFiles: list[str], savedFiles: dict[str, bytes]) -> None:
    for fl in trackedFiles:
        debug_print(f"Collecting {fl}")
        with open(fl, "rb") as f:
            savedFiles[fl] = f.read()

def revertFile(fl: str, savedFiles: dict[str, bytes]) -> None:
    with open(fl, "wb") as f:
        f.write(savedFiles[fl])

def checkFiles(trackedFiles: list[str], hashes: dict[str, str], savedFiles: dict[str, bytes]) -> None:
    for fl in trackedFiles:
        debug_print(f"Checking {fl}")
        if hashFile(fl) != hashes[fl]:
            debug_print(f"File {fl} has changed, reverting to saved version")
            revertFile(fl, savedFiles)

def mpUntrackFiles(trackedFiles: list[str], hashes: dict[str, str], savedFiles: dict[str, bytes], fl) -> None:
    trackedFiles.remove(fl)
    del hashes[fl]
    del savedFiles[fl]

def mpCheckFiles(pipe: mp.Pipe) -> None:
    trackedFiles = list[str]
    hashes: dict[str, str]
    savedFiles: dict[str, bytes]
    buf = list[str]

    while True:
        buf.append(pipe.read().split(";")[1]()

        if inpt.split()[1] == "untrack":
            mpUntrackFiles(trackedFiles, hashes, savedFiles, inpt.split()[2])
        elif inpt.split()[1] == "track":
            trackedFiles.append(inpt.split()[2])
            hashes[inpt.split()[2]] = hashFile(inpt.split()[2])
            with open(inpt.split()[2], "rb") as f:
                savedFiles[inpt.split()[2]] = f.read()
        checkFiles(trackedFiles, hashes, savedFiles)
        time.sleep(10)

def Loop(trackedFiles: list[str], hashes: dict[str, str], savedFiles: dict[str, bytes], pipe: mp.Pipe) -> None:
    while True:
        inpt = input("Enter command:")
        if inpt.lower() == "done":
            break
        elif inpt.lower() == "track":
            addFile(trackedFiles, pipe)
        elif inpt.lower() == "untrack":
            removeFile(trackedFiles, pipe)
        elif inpt.lower() == "help":
            print(f"Commands: track, untrack, help, done")
        


def main():
    checkPlatform()
    pipe = mp.Pipe()
    p = mp.Process(target=mpCheckFiles, args=(pipe, ))
    p.start()
    Loop()
    p.join()
    

if __name__ == '__main__':
    main()



    # Github CoPilot is fucking SCARY