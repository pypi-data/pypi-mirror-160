
# states
enabled = 1

# unit types
unitTypeHeat = 0
unitTypeCool = 1

from ha import *

# control for a heat pump
class HeatPumpControl(Control):
    def __init__(self, name, interface, unitControl, reverseControl, unitType,
                **kwargs):
        Control.__init__(self, name, interface, **kwargs)
        self.className = "Control"
        self.unitControl = unitControl              # the control for the unit
        self.reverseControl = reverseControl        # the control for the reversing valve
        self.unitType = unitType                    # type of unit: 0=heater, 1=cooler
        self.controlState = off                     # state of this control

    def getState(self, wait=False, missing=None):
        debug('debugState', self.name, "getState ", self.controlState)
        return self.controlState

    def setState(self, state, wait=False):
        debug('debugState', self.name, "setState ", state)
        self.unitControl.setState(state)
        if state == 1:
            self.reverseControl.setState(1 - self.unitType) # reverse valve on is heat
        else:
            self.reverseControl.setState(0)
        self.controlState = state
        self.notify()
