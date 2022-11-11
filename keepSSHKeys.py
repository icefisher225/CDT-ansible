import os, sys, multiprocessing, threading, math, time, subprocess, hashlib


def main():
    trackedFiles = list()
    hashes = dict()
    savedFiles = dict()
    inputFiles(trackedFiles)
    hashFiles(trackedFiles, hashes)
    while True:
        checkFiles()

def inputFiles(trackedFiles):
    while True:
        fl = input("File you want saved: ")
        try:
            subprocess.check_output(f"cat {fl} > /dev/null", shell=True)
        except:
            print(f"File {fl} does not exist, please try again")
        
        trackedFiles.append(fl)

        print(f"Files to be saved: {trackedFiles}")
        done = input("Press enter to continue, or type 'done' to finish")
        if done.lower() == "done":
            break

def hashFile(fl):
    return hashlib.sha256(open(fl, "rb").read()).hexdigest()

def hashFiles(trackedFiles, hashes):
    for fl in trackedFiles:
        print(f"Hashing {fl}")
        hashes[fl] = hashFile(fl)

def collectFiles(trackedFiles, savedFiles):
    for fl in trackedFiles:
        print(f"Collecting {fl}")
        savedFiles[fl] = open(fl, "rb").read()

def checkFiles(trackedFiles, hashes, savedFiles):
    for fl in trackedFiles:
        print(f"Checking {fl}")
        if hashFile(fl) != hashes[fl]:
            print(f"File {fl} has changed, reverting to saved version")
            open(fl, "wb").write(savedFiles[fl])
    time.sleep(1)

if __name__ == '__main__':
    main()