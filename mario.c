#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h;

    //Checks if height is in the valid range
    do
    {
        h = get_int("Height: ");
    }
    while ((h < 1) || (h > 8));

    for (int i = 1; i < (h + 1); i++)
    {
        for (int l = 0; l < (h - i); l++) //Adds the required spaces
        {
            printf(" ");
        }
        for (int j = 0; j < i; j++) // Prints appropriate number of hashes
        {
            printf("#");
        }
        printf("\n"); //Adds a new line
    }
}