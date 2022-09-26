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

    int k = atoi(argv[1]);
    if (k < 0)
    {
        printf("Usage: ./caesar [key]\n");
        return 2;
    }

    //Ask user for plaintext
    string p = get_string("Plaintext : ");
    printf("Ciphertext: ");
    for (int i = 0; i < strlen(p); i++)
    {
        char c = p[i];
        char h = c + k;
        if (isupper(c))
        {
            if (h > 90)
            {
                h-=26;
            }
        }

        else if (islower(c))
        {
            if (h > 122)
            {
                h-=26;
            }
        }

        else
        {
            h = c;
        }

        //Printing each coded character out
        printf("%c", h);
    }
    printf("\n");
}