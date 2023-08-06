monitorInterval = 10

import time
from ha import *

# Renogy charge controller
class RenogySensor(Sensor):
    def __init__(self, name, interface, addr, mask=0xffff, shift=0,
            **kwargs):
        Sensor.__init__(self, name, interface, addr, **kwargs)
        self.className = "Sensor"
        self.mask = mask
        self.shift = shift

    def getState(self, missing=0.0):
        state = self.interface.read(self.addr)
        if state:
            if self.addr == 0x0120:  # charge mode
                return int(state) & 0xff
            else:
                try:
                    return float((state >> self.shift) & self.mask) * self.factor + self.offset
                except Exception as ex:
                    log(self.name, str(ex), state, self.shift, self.mask, self.factor)
                    return 0.0
        else:
            return 0.0

# a control that switches between a power supply and solar panels to charge a backup battery
class BackupChargingControl(Control):
    def __init__(self, name, interface,
                batteryChargeSensor, relayControl,
                highBatteryChargeLevel=90,
                lowBatteryChargeLevel=50,
                start=True, **kwargs):
        Control.__init__(self, name, interface, **kwargs)
        self.className = "Control"
        self.batteryChargeSensor = batteryChargeSensor          # the sensor for the battery percentage of charge
        self.relayControl = relayControl                        # the control that switches the relay
        self.highBatteryChargeLevel = highBatteryChargeLevel    # switch to solar at or above this charge percent
        self.lowBatteryChargeLevel = lowBatteryChargeLevel      # switch from solar to grid at this charge percent
        self.active = 1                                         # state of this control
        if start:
            self.start()

    def start(self):
        startThread("chargingMonitor", self.chargingMonitor)

    def chargingMonitor(self):
        while True:
            debug("debugChargingMonitor", "chargingMonitor", self.active, self.batteryChargeSensor.getState(), self.relayControl.getState())
            if self.active:
                # switch to solar if the battery is sufficiently charged
                if self.batteryChargeSensor.getState() >= self.highBatteryChargeLevel:
                    self.relayControl.setState(1)
                # switch to power supply if battery charge drops below minimum threshold
                if self.batteryChargeSensor.getState() <= self.lowBatteryChargeLevel:
                    self.relayControl.setState(0)
            time.sleep(monitorInterval)

    def getState(self, wait=False, missing=None):
        debug('debugState', self.name, "getState ", self.active)
        return self.active

    def setState(self, state, wait=False):
        debug('debugState', self.name, "setState ", state)
        self.active = state

# a control that monitors the charging mode and resets current sensors when the battery is fully charged
class BackupChargeLevelReset(Control):
    def __init__(self, name, interface,
                batteryChargeModeSensor, currentSensors,
                start=True, **kwargs):
        Control.__init__(self, name, interface, **kwargs)
        self.className = "Control"
        self.batteryChargeModeSensor = batteryChargeModeSensor  # the sensor for the charge mode
        self.currentSensors = currentSensors                    # the current sensors
        self.active = 1                                         # state of this control
        self.lastChargeMode = 0                                 # previous charge mode
        if start:
            self.start()

    def start(self):
        startThread("chargeLevelReset", self.chargeLevelReset)

    def chargeLevelReset(self):
        while True:
            debug("debugChargeLevelReset", "chargeLevelReset", self.active, self.batteryChargeModeSensor.getState(), self.lastChargeMode)
            if self.active:
                # reset current sensors when charge mode switches from constant to absorbtion
                chargeMode = self.batteryChargeModeSensor.getState()
                if chargeMode != self.lastChargeMode:
                    if (self.lastChargeMode == 6) and (chargeMode == 4):
                        self.currentSensors.setState(0)
                    self.lastChargeMode = chargeMode
            time.sleep(monitorInterval)

    def getState(self, wait=False, missing=None):
        debug('debugState', self.name, "getState ", self.active)
        return self.active

    def setState(self, state, wait=False):
        debug('debugState', self.name, "setState ", state)
        self.active = state

# sensor to calculate battery charge percentage based on capacity and discharge
class BatteryChargeSensor(Sensor):
    def __init__(self, name, interface,
                dischargeSensor, capacity, **kwargs):
        Sensor.__init__(self, name, interface, **kwargs)
        self.className = "Sensor"
        self.dischargeSensor = dischargeSensor
        self.capacity = capacity

    def getState(self, missing=0.0):
        discharge = self.dischargeSensor.getState(missing=0.0)
        return (self.capacity + discharge) * 100./self.capacity
