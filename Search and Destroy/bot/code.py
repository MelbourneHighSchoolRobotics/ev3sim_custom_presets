from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B

x = int(input())
y = int(input())

print(f"Green X={x}")
print(f"Green Y={y}")

# You'll need to add the motors onto the bot.
motor1 = LargeMotor(OUTPUT_A)
motor2 = LargeMotor(OUTPUT_B)

# Step 1: Move to the right.

# Step 2: Rotate to face downards.

# Step 3: Move down to the flag at position x, y
