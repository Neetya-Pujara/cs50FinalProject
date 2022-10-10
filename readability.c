#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    string input = get_string("Text: ");
    int letters = 0;
    int words = 1;
    int sentences = 0;
    for (int i = 0; i < strlen(input); i++)
    {
        if (isalpha(input[i]))
        {
            letters++;
        }

        else if (input[i] == 32)
        {
            words++;
        }

        else if ((input[i] == '.') || (input[i] == '!') || (input[i] == '?'))
        {
            sentences++;
        }
    }

    float l = letters / (float) words * 100;
    float s = sentences / (float) words * 100;
    int index = round(0.0588 * l - 0.296 * s - 15.8);

    if (index < 1)
    {
        printf("Before Grade 1\n");
        return 0;
    }

    if (index > 16)
    {
        printf("Grade 16+\n");
        return 0;
    }

    printf("Grade %i\n", index);
}