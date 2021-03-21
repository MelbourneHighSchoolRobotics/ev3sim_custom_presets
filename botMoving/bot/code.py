from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B

horizontalMotor = LargeMotor(OUTPUT_A)
verticalMotor = LargeMotor(OUTPUT_B)

x = int(input())

print(f"Green X={x}")
print(f"Green Y=???")
