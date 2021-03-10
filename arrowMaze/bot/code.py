import time
from ev3dev2.motor import LargeMotor
from ev3sim.code_helpers import EventSystem, wait_for_tick

grid = []
def on_spawn(data):
    global grid
    grid = data["grid"]
EventSystem.on_spawn = on_spawn
wait_for_tick()
EventSystem.handle_events()

topMotor = LargeMotor("outA")
botMotor = LargeMotor("outB")

# Here's some helper functions to reduce some of the trail and error.

def wait():
    time.sleep(0.1)

def rotate(neg):
    # rotate(1): clockwise 90 degrees.
    # rotate(-1): counterclockwise 90 degrees.
    topMotor.on_for_seconds(neg * 10, 1.6, block=False)
    botMotor.on_for_seconds(-neg * 10, 1.6)
    wait()

def forward():
    botMotor.on_for_seconds(20, 1.9, block=False)
    topMotor.on_for_seconds(20, 1.9)
    wait()

# Your code goes here
print("Grid is", grid)
forward()
rotate(-1)
forward()
