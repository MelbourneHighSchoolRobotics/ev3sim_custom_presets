import time
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from ev3sim.code_helpers import wait_for_tick

wait_for_tick()
cs = ColorSensor(INPUT_1)

# Your code goes here!
r, g, b = cs.rgb
print("Values:", r, g, b)
if "???":
    print("Is red!")
# Handle blue, green and yellow as well.

# Wait for two seconds.
time.sleep(2)

# Do it two more times.
