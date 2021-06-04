from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import UltrasonicSensor

# You'll need to add the motors, and sensors, onto the bot.
motor1 = LargeMotor(OUTPUT_A)
motor2 = LargeMotor(OUTPUT_B)

sensor = UltrasonicSensor(INPUT_1)

# TODO: Figure out how close I am to the spaceship, and move away / closer.
