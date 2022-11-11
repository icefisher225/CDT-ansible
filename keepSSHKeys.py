import os, sys, multiprocessing, threading, math, time, subprocess, hashlib


def main():
    trackedFiles = list()
    hashes = dict()
    inputFiles(trackedFiles)
    hashFiles(trackedFiles, hashes)

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

def hashFiles(trackedFiles, hashes):
    for fl in trackedFiles:
        print(f"Hashing {fl}")
        hashes[fl] = hashlib.sha256(open(fl, "rb").read()).hexdigest()

    

if __name__ == '__main__':
    main()