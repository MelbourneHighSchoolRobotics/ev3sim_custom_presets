# First, read in the weather for all the days of the month.
number_of_days = int(input())
days = []
counter = 0
while counter < number_of_days:
    days.append(input())
    counter += 1

# Next, tell me (Using splices, and `join`):

# 1. What the weather was for the second, third and fourth days?
print(" ".join(["Sunny", "Snow", "Rain"]))

# 2. What the weather was for the last two days?
print(" ".join(["Sunny", "Snow", "Rain"]))

# 3. What the weather was for the first two fridays? (Assuming that every month starts on a monday)
print(" ".join(["Sunny", "Snow", "Rain"]))

# Extension:

# 4. What the weather was for the 2nd last, 3rd last and 4th last days (in that order)?
print(" ".join(["Sunny", "Snow", "Rain"]))
