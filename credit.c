#include <cs50.h>
#include <stdio.h>

void invalid(void);

int main(void)
{
    // input
    long number = get_long("Number: ");

    if (number <= 0)
    {
        invalid();
        return 0;
    }

    // checksum
    long previous = 0;
    int sum1 = 0;
    int sum2 = 0;
    bool whichSum = true;
    bool done = false;
    for (long curr = 10; done == false; curr*=10)
    {
        if (number / curr <= 0)
        {
            done = true;
        }
        if (whichSum == true)
        {
            sum1 += ((number % curr) - previous) / (curr/10);
            whichSum = false;
        }
        else
        {
            int num = (((number % curr) - previous) / (curr/10)) * 2;
            if (num/10 == 0)
            {
                sum2 += num;
            }
            else
            {
                sum2 += num / 10 + num % 10;
            }
            whichSum = true;
        }
        previous = number % curr;
    }

    // verifying checksum
    if ((sum2 + sum1) % 10 != 0)
    {
        invalid();
    }

    // in case of valid checksum
    else
    {
        //american express
        if (number / 100000000000000 > 0 && number / 1000000000000000 == 0)
        {
            int second = number / 1000000000000;
            if (second == 34 || second == 37)
            {
                printf("AMERICAN EXPRESS\n");
            }
            else
            {
                invalid();
            }
        }

        //visa or mastercard
        else if (number / 1000000000000000 > 0 && number / 10000000000000000 == 0)
        {
            int second = number / 100000000000000;
            if (second / 10 == 4)
            {
                printf("VISA\n");
            }
            else if (second == 51 || second == 52 || second == 53 || second == 54 || second == 55)
            {
                printf("MASTERCARD\n");
            }
            else
            {
                invalid();
            }
        }

        //visa
        else if (number / 1000000000000 > 0 && number / 10000000000000 == 0)
        {
            int first = number / 1000000000000;
            if (first == 4)
            {
                printf("VISA\n");
            }
            else
            {
                invalid();
            }
        }

        // invalid
        else
        {
            invalid();
        }
    }
}

void invalid(void)
{
    printf("INVALID\n");
}
