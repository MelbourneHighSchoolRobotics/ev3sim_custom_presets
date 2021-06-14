import time
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B

m_l = LargeMotor(OUTPUT_A)
m_r = LargeMotor(OUTPUT_B)

# This line just lets us receive a list. Don't worry about it :)
commands = eval(input())

robot_speed = 26.316

print("Commands are", commands)

i = 1
# TODO: Mention len.
while i < len(commands):
    direction = commands[i][0]
    distance = commands[i]

    if direction == "Left":
        m_l.on_for_seconds(-20, 1.08, block=False)
        m_r.on_for_seconds(20, 1.08)
    elif direction == "Right":
        m_l.on_for_seconds(20, 1.08, block=False)
        m_r.on_for_seconds(-20, 1.08)

    # Some delays to ensure sliding doesn't affect our trajectory.
    time.sleep(0.1)
    m_l.on_for_seconds(50, distance / robot_speed, block=False)
    m_r.on_for_seconds(50, distance / robot_speed)
    time.sleep(0.1)

    i += 1
