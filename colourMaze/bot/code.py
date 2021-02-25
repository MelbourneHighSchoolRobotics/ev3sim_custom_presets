import time
from ev3dev2.motor import LargeMotor
from ev3dev2.sensor.lego import ColorSensor

sideMotor = LargeMotor("outA")
verticalMotor = LargeMotor("outB")
color = ColorSensor("in1")
