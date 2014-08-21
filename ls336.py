#!/usr/bin/env python

# make sure bridge.py is on the python path
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from bridge import Connect

# If the control computer is disconnected, then when it is
# reconnected it will be expecting to send a command to
# the bridge, not read a response.  So set it up with retry="read"
# so that on readline error it reopens the channel but ignore write
# immediately.  Similarly, if the Lakeshore is disconnected, it 
# will be expecting to receive a new command not send a response, 
# so retry the write command.
RS232 = Connect("/dev/ttyOutputRS232", retry="read",
    baudrate=9600, parity='O', bytesize=7, stopbits=1)
lakeshore = Connect("/dev/ttyLakeshore336", retry="write",
    baudrate=57600, parity='O', bytesize=7, stopbits=1)

while True:
    print "Waiting for next command..."
    command = RS232.readline()
    print "Command",command.strip()
    lakeshore.write(command)
    if '?' in command:
        print "Waiting for reply..."
        reply = lakeshore.readline()
        print "Reply",reply.strip()
        RS232.write(reply)

