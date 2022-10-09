#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int h;
    do
    {
        h = get_int("Height: ");
    }
    while ((h < 1) || (h > 9));

    for (int i = 1; i < (h + 1); i++)
    {
        for (int l = 0; l < (h - i); l++)
        {
            printf(" ");
        }
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}