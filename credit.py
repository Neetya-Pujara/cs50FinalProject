# import necessary functions
from cs50 import get_int

# Prompt user for credit card number
number = str(get_int("Number: "))

# Check if number is valid
names = ['AMEX', 'VISA', 'MASTERCARD']
cards = ['3', '4', '5']
valid = False
sum1 = []
total = 0
for i in range(len(number)):
    if not (i % 2) == 0:
        total += int(number[i])
    else:
        x = int(number[i]) * 2
        if x > 10:
            sum1.append(int(str(x)[0]))
            sum1.append(int(str(x)[1]))
        else:
            sum1.append(x)
total += sum(sum1)
tmp = str(total)
if tmp[len(tmp) - 1] == '0':
    valid = True
if valid == False:
    print("INVALID")
    exit()
for n in range(3):
    if cards[n] == number[0]:
        print(names[n])
        break

