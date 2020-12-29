from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor
from ev3sim.code_helpers import wait_for_tick, CommandSystem

wait_for_tick()
cs = ColorSensor(INPUT_1)

# Your code goes here!
print(cs.rgb)
colour = "Red"
CommandSystem.send_command(CommandSystem.TYPE_CUSTOM, f"Colour: {colour}")
