from ev3sim.code_helpers import wait_for_tick
from ev3dev2.motor import LargeMotor
from ev3dev2.sensor import Sensor

motor = LargeMotor("outA")
# Put in the right values here.
ir = Sensor("in1", driver_name=???)
ir.mode = ???

# Write some code here!
