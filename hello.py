#imports get_string
from cs50 import get_string

#Inputs user for their name
name = get_string("What's your name? ")

#Prints their name along with hello {name}
print(name)
print(f"hello, {name}")