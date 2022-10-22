# Import get_int
from cs50 import get_int

# Input height from the user
height = get_int("Height: ")

# Implement the pattern
for i in range(height):
    spaces = " " * (height - (i + 1))
    hashes = "#" * (i + 1)

    # Join the variables through a formatted string
    print(f"{spaces}{hashes} {hashes}")
