# Logging functions

import syslog
import os
import time
import threading
import traceback
from .environment import *

# standard timestamp
def timeStamp(fmt):
    return time.strftime(fmt, time.localtime())

# log a message to syslog or stdout
def log(*args):
    message = args[0]+" "   # first argument is the object doing the logging
    for arg in args[1:]:
        message += arg.__str__()+" "
    if sysLogging:
        syslog.syslog(message)
    else:
        print(timeStamp("%b %d %H:%M:%S")+" "+message)

# log the traceback for an exception
def logException(name, ex):
    tracebackLines = traceback.format_exception(None, ex, ex.__traceback__)
    log(name+":")
    for tracebackLine in tracebackLines:
        log(tracebackLine)

# thread object that logs a stack trace if there is an uncaught exception
class LogThread(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.runTarget = self.run
        self.run = self.logThread

    def logThread(self):
        try:
            self.runTarget()
        except Exception as ex:
            logException("thread "+threading.currentThread().name, ex)

# convenience function to create and start a thread
def startThread(name, target, **kwargs):
    thread = LogThread(name=name, target=target, **kwargs)
    thread.start()
