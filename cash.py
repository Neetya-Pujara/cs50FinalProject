from cs50 import get_float

def main():
    money = [25, 10, 5, 1]
    total = 0
    change = int(input_change() * 100)
    for n in range(4):
        if change > (money[n] - 1):
            total += (change - (change % (money[n]))) / money[n]
        else:
            total += 0
        change -= (number[n] * money[n])

    print(total)


def input_change():
    while True:
        # Input user for change owed
        change = get_float("Change owed: ")
        if change > 0:
            break
        print("Enter a valid (positive) value!")
    return change

main()
