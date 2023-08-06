import os
import subprocess
import time
from ha import *

class VideoInterface(Interface):
    def __init__(self, name, interface, videoControl, event=None):
        Interface.__init__(self, name, interface=interface, event=event)
        self.videoControl = videoControl
        self.state = 0
        self.pid = 0

    def read(self, addr):
        return self.state

    def write(self, addr, value):
        if value != self.state:
            if value:
                video = self.videoControl.getState()
                cmd = "/usr/bin/mplayer -really-quiet -fs -lavdopts threads=4 -loop 0 -vo fbdev /video/"+video+".mp4"
                self.pid = subprocess.Popen(cmd, shell=True).pid+1
                log("pid", self.pid)
            else:
                if self.pid:
                    pid = subprocess.Popen("kill "+str(self.pid), shell=True)
                time.sleep(1)
                pid = subprocess.Popen("dd if=/dev/zero of=/dev/fb0", shell=True)
                pid = subprocess.Popen("setterm -cursor off > /dev/tty1", shell=True)
            self.state = value
