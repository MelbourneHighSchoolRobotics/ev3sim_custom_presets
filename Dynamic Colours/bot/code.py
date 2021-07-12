import time
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from ev3sim.code_helpers import wait_for_tick

wait_for_tick()
cs = ColorSensor(INPUT_1)

# Should be "This is what white looks like"
msg = input()

# Do we want to do something here now that we are looking at pure white?

print("Ready!")

# The colours start coming in input.
