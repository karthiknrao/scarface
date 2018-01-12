import os
import time
from subprocess import Popen, PIPE
import sys

port = int(sys.argv[1])

def reversessh(port):
    cmd = [ "ssh", "-i", ".pem", "-fN", "-R", "%d:localhost:22" %(port), "ubuntu@" ]
    print(cmd)
    sshp = Popen( cmd, stdin=PIPE, stdout=PIPE )
    pid = sshp.pid
    return pid

def getsshpid(port):
    cmd = [ 'ps', 'aux' ]
    psout = Popen(cmd, stdin=PIPE, stdout=PIPE)
    output = psout.communicate()[0]
    lines = output.split('\n')
    pattern = '%d:localhost:22' % port
    validlines = [ i for i,x in enumerate(lines) if pattern in x ]
    if len(validlines) > 0:
        sshpid = int(lines[validlines[0]].split()[1])
    else:
        sshpid = None
    return sshpid

def checkprocess(pid):
    if pid == None:
        return False
    procpath = '/proc/%s' % (str(pid))
    if os.path.exists(procpath):
        return True
    else:
        return False
    
reversessh(port)
time.sleep(2)
pid = getsshpid(port)
while True:
    print('Current pid ', pid)
    time.sleep(120)
    if not checkprocess(pid):
        reversessh(port)
        time.sleep(2)
        pid = getsshpid(port)
    else:
        print('Already Running')
