"""
Reliable version of pyserial
"""

from serial import Serial, SerialException
import time

class Connect:
    """
    Serial port connection.

    The interface is identical to the pyserial Serial class,
    with the addition of a *retry* keyword which indicates that
    the serial connection should be reopened automatically.

    Use *retry="write"* to reopen on write, *retry="read"* to reopen
    on read, or the default *retry="readwrite"* to reopen on read
    and write failure.

    This allows the user to unplug the serial cable and plug it
    back in again, or equivalently, shut off the serial device
    and turn it back on again, for example, as a way to reset
    its state.

    Only the *readline* and *write* methods are supported.
    """
    def __init__(self, *args, **kw):
        self.retry = kw.pop('retry','readwrite')
        self.args = args
        self.kw = kw
        self.channel = None

    def write(self, str):
        while True:
            try:
                if self.channel is None:
                    self.channel = Serial(*self.args, **self.kw)
                    self.channel.flushInput()
                return self.channel.write(str)
            except SerialException, exc:
                if self.channel is not None:
                    try: self.channel.close()
                    except: pass
                    self.channel = None
                print exc
                if "write" not in self.retry:
                    return 0
                print "Restarting in 1s..."
                time.sleep(1)

    def readline(self):
        while True:
            try:
                if self.channel is None:
                    self.channel = Serial(*self.args, **self.kw)
                    self.channel.flushOutput()
                return self.channel.readline()
            except SerialException, exc:
                if self.channel is not None:
                    try: self.channel.close()
                    except: pass
                    self.channel = None
                print exc
                if "read" not in self.retry:
                    return ""
                print "Restarting in 1s..."
                time.sleep(1)
