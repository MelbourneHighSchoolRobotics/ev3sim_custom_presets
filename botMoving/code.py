from ev3dev2.motor import LargeMotor
from ev3sim.code_helpers import format_print, wait_for_tick, EventSystem

x, y = 0, 0
def on_spawn(data):
    global x, y
    x, y = data["position"]

EventSystem.on_spawn = on_spawn
wait_for_tick()
EventSystem.handle_events()

target_string = "{x}, {y}".format(x=x, y=y)

format_print("The target is at <b>" + target_string + "</b>")
wait_for_tick()

sideMotor = LargeMotor("outA")
verticalMotor = LargeMotor("outB")

# Your code goes here!
# verticalMotor.on_for_rotations(100, 15)

wait_for_tick()
