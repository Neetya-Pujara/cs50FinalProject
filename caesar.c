#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Enter one command line argument (for the key)!\n");
        return 1;
    }

    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (isdigit(argv[1][i]) == 0)
        {
            printf("Enter a integer key!\n");
            return 1;
        }
    }

    int key = atoi(argv[1]);

    string plain = get_string("Plaintext: ");

    for (int i = 0; i < strlen(plain); i++)
    {
        if (isalpha(plain[i]))
        {
            int c = plain[i] + key;

            if (isupper(plain[i]))
            {
                while (c > 90)
                {
                    c-=26;
                }
                plain[i] = c;
            }

            if (islower(plain[i]))
            {
                while (c > 122)
                {
                    c-=26;
                }
                plain[i] = c;
            }
        }
    }
    printf("Ciphertext: %s\n", plain);
}