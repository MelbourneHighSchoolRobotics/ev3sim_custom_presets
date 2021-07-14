from ev3sim.code_helpers import wait_for_tick
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor import Sensor, INPUT_1

m_l = LargeMotor(OUTPUT_A)
m_r = LargeMotor(OUTPUT_B)
compass = Sensor(INPUT_1, driver_name="ht-nxt-compass")

robot_speed = 26.316

compass.command = "BEGIN-CAL"
compass.command = "END-CAL"

n = int(input())

commands = []
x = 0
while x < n:
    msg = input().split()
    name = msg[0]
    distance = int(msg[2])
    degrees = int(msg[5])
    commands.append((name, distance, degrees))
    x = x + 1

goto = input()
wanted = goto.split()[2]

print(goto)

# Now, find the command which has name == wanted.
x = 0
while x < n:
    if commands[x][0] == wanted:
        # We want to go here!
        distance = commands[x][1]
        degrees = commands[x][2]
        print(f"{wanted} is {distance} away at {degrees} degrees")

        # Make the robot turn so the compass reads the correct angle
        # Start turning clockwise very slowly.
        while True:
            compass_angle = compass.value()
            if degrees - 1 <= compass_angle <= degrees + 1:
                break
            # We also need to be careful when degrees is 0. A compass angle of 359 is super close,
            # and so we need to check this case separately
            elif degrees == 0 and compass_angle >= 359:
                break
            difference = compass_angle - degrees
            if difference > 180:
                difference = difference - 360
            elif difference < -180:
                difference = difference + 360
            # Now difference is in between -180 and 180.
            # If it's negative, we need to turn clockwise
            if difference < 0:
                # Motors are more powerful when difference is large
                m_l.on((difference - 20) / 5)
                m_r.on(-(difference - 20) / 5)
            else:
                # Motors are more powerful when difference is large
                m_l.on((difference + 20) / 5)
                m_r.on(-(difference + 20) / 5)
            wait_for_tick()
        # Go forwards
        m_l.on_for_seconds(50, distance / robot_speed, block=False)
        m_r.on_for_seconds(50, distance / robot_speed)
    x = x + 1
