# Send RGB light colors over a serial interface
from ha import *

syn = 0x16
def checksum(digits):
    sum = 0
    for digit in digits:
        sum += digit
    return sum % 256

class SerialRGBInterface(Interface):
    def __init__(self, name, interface, **kwargs):
        Interface.__init__(self, name, interface=interface, **kwargs)
        self.bytes = bytearray()

    def write(self, addr, value):
        debug("debugHolidayLights", self.name, "write", value)
        self.bytes.append((value>>16) & 0xff)     # red
        self.bytes.append((value>>8) & 0xff)      # green
        self.bytes.append(value & 0xff)           # blue
        return True

    def show(self):
        msg  = bytearray([syn, syn, syn])                   # sync bytes
        msg += len(self.bytes).to_bytes(1, "little")        # data length
        msg += self.bytes                                   # data
        msg += checksum(self.bytes).to_bytes(1, "little")   # checksum
        debug("debugHolidayLights", self.name, "show", msg)
        self.interface.write(0, msg)
        self.bytes = bytearray()
        return True
