# Serena's metal sheet construction code.
l = int(input("What is l: "))
w = int(input("and w: "))

# Double the length
w = l * 2

# Get the perimeter of this doubled sheet
perimeter = 2 * w + 2 * l

# Get the area
area = w * l

print(f"Area is {area}.")
print(f"Double length perimeter is {perimeter}.")


# Print the sum
# This should be 52=24+28 with the l=4 and w=6 :(
print(f"And so the cost is {area * perimeter}.")