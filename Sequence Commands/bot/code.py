import time
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B

m_l = LargeMotor(OUTPUT_A)
m_r = LargeMotor(OUTPUT_B)

number_commands = int(input())
commands = []
x = 0
while x < number_commands:
    msg = input().split()
    # Move {direction} for {distance}
    direction = msg[1]
    # This is a whole number! Use int.
    distance = int(msg[3])
    # Lists in lists!
    commands.append([distance, direction])
    x = x + 1


robot_speed = 26.316

print("Commands are", commands)

i = 1
while i < len(commands):
    # What is commands[i] here?
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
