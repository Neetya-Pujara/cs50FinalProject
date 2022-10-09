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
        if (isupper(plain[i]) != 0)
        {
            plain[i] += key;
            while (plain[i] > 90)
            {
                plain[i] -= 26;
            }
        }

        if (islower(plain[i]) != 0)
        {
            plain[i] += key;
            while (plain[i] > 122)
            {
                plain[i] -= 26;
            }
        }
    }
    printf("Ciphertext: %s\n", plain);
}