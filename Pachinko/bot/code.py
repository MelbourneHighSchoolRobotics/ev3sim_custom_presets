position = int(input("What location did the ball fall into?"))

# 3 errors below, can you fix them please :(

if position <= 19:
    if position >= 14:
        print("Jumbo Prize!")
    else:
        if position < 5:
            print("Large Prize!")
        else:
            print("Small Prize!")
else:
    if position <= 23:
        print("Medium Prize!")
    print("Teensy Prize!")
