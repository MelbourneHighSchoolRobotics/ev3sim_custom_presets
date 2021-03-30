import time
from ev3dev2.motor import LargeMotor
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor
from ev3sim.code_helpers import CommandSystem

topMotor = LargeMotor("outA")
botMotor = LargeMotor("outB")
color = ColorSensor("in1")
ultrasonic = UltrasonicSensor("in2")

# Here's some helper functions to reduce some of the trial and error.
# Jump to the bottom of the file to seem how to use them.

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

pword = "LRS"

# Your code goes here!

forward()
rotate(-1)
forward()

print(f"Password is {pword}")
CommandSystem.send_command(CommandSystem.TYPE_CUSTOM, pword)
