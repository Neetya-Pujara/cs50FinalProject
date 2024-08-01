#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // input
    int change;
    do
    {
        change = get_int("Change owed: ");
    }
    while (change < 0);

    int coins = 0;

    // quarters
    int quarters = change / 25;
    coins += quarters;
    change -= quarters * 25;

    // dimes
    int dimes = change / 10;
    coins += dimes;
    change -= dimes * 10;

    // nickels
    int nickels = change / 5;
    coins += nickels;
    change -= nickels * 5;

    // pennies
    coins += change;

    printf("%i\n", coins);
}
