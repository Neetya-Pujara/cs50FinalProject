#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar [key]\n");
        return 1;
    }

    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (isdigit(argv[1][i]) == 0)
        {
            return 1;
        }
    }
    int k = atoi(argv[1]);
    if (k < 0)
    {
        printf("Usage: ./caesar [key]\n");
        return 1;
    }

    //Ask user for plaintext
    string p = get_string("Plaintext : ");
    printf("Ciphertext: ");
    for (int i = 0; i < strlen(p); i++)
    {
        char c;
        if (isupper(p[i]))
        {
            c = p[i] + k;
            if (c > 90)
            {
                c-=26;
            }
        }

        else if (islower(p[i]))
        {
            c = p[i] + k;
            if (c > 122)
            {
                c-=26;
            }
        }

        else
        {
            c = p[i];
        }

        //Printing each coded character out
        printf("%c", c);
    }
    printf("\n");
}