import math, time, subprocess, hashlib

DEBUG_PRINT = True

def debug_print(*args: str)-> None:
    if DEBUG_PRINT:
        print(*args)

def inputFiles(trackedFiles: list[str])-> None:
    while True:
        fl = input("File you want saved: ")
        try:
            subprocess.check_output(f"cat {fl} > /dev/null", shell=True)
        except:
            debug_print(f"File {fl} does not exist, please try again")
        
        trackedFiles.append(fl)

        debug_print(f"Files to be saved: {trackedFiles}")
        done = input("Press enter to continue, or type 'done' to finish")
        if done.lower() == "done":
            break

def hashFile(fl: str) -> str:
    return str(hashlib.sha256(open(fl, "rb").read()).hexdigest())

def hashFiles(trackedFiles: list[str], hashes: dict[str, str]) -> None:
    for fl in trackedFiles:
        debug_print(f"Hashing {fl}")
        hashes[fl] = hashFile(fl)

def collectFiles(trackedFiles: list[str], savedFiles: dict[str, bytes]) -> None:
    for fl in trackedFiles:
        debug_print(f"Collecting {fl}")
        savedFiles[fl] = open(fl, "rb").read()

def checkFiles(trackedFiles: list[str], hashes: dict[str, str], savedFiles: dict[str, bytes]) -> None:
    for fl in trackedFiles:
        debug_print(f"Checking {fl}")
        if hashFile(fl) != hashes[fl]:
            debug_print(f"File {fl} has changed, reverting to saved version")
            open(fl, "wb").write(savedFiles[fl])
    time.sleep(1)

def main():
    trackedFiles = list[str]
    hashes = dict[str, str]
    savedFiles = dict[str, bytes]
    inputFiles(trackedFiles)
    hashFiles(trackedFiles, hashes)
    collectFiles(trackedFiles, savedFiles)
    while True:
        checkFiles(trackedFiles, hashes, savedFiles)

if __name__ == '__main__':
    main()