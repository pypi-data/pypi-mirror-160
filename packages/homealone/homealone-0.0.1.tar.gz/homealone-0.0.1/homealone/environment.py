# Global variables that define the environment

import os
import socket
import platform

# determine the hardware this is running on
machine = platform.machine()
if machine in ["armv6l", "armv6l"]:
    platformType = "rpi"
elif machine in ["esp8266", "esp32"]:
    platformType = "esp"
elif machine in ["x86_64"]:
    platformType = "mac"
else:
    platformType = "unknown"

# directory structure
hostname = socket.gethostname()
rootDir = os.path.expanduser("~")+"/"
configDir = rootDir+"conf/"
keyDir = rootDir+"keys/"
stateDir = rootDir+"state/"
soundDir = rootDir+"sounds/"
dataLogDir = "data/"
dataLogFileName = ""

# Localization - define these in the config file
    # latLong = (0.0, 0.0)
    # elevation = 0 # elevation in feet
    # tempScale = "F"

# global variables that must be set here
sysLogging = True
