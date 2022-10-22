# Import get_int
from cs50 import get_int

while True:
    # Input height from the user
    height = get_int("Height: ")

    #Rejecting less than one input
    if (height > 0) and (height < 9):
        break

    print("Height should be between 1 and 8!")

# Implement the pattern
for i in range(height):
    spaces = " " * (height - (i + 1))
    hashes = "#" * (i + 1)

    # Join the variables through a formatted string
    print(f"{spaces}{hashes} {hashes}")
