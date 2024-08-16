#include <cs50.h>
#include <stdio.h>
#include <ctype.h>

int length(string str);
string cipher(string text, string key);
string tolowerkey(string key);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage : ./substitution key\n");
        return 1;
    }

    else if (length(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    string key = argv[1];
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: %s\n", cipher(plaintext, key));
}

string tolowerkey(string key)
{
    for (int i = 0, len = length(key); i < len; i++)
    {
        key[i] = tolower(key[i])
    }
}
string cipher(string text, string key)
{
    string ciphertext = "";
    for (int i = 0, len = length(text); i < len; i++)
    {
        if (text[i] >= 'a' && text[i] <= 'z')
        {
            ciphertext += key[text[i]-97];
        }
        else if (text[i] >= 'A' && text[i] <= 'Z')
        {
            ciphertext += toupper(key[text[i]-65]);
        }
        else
        {
            ciphertext += text[i];
        }
    }
    return ciphertext;
}

int length(string str)
{
    int len = 0;
    for (int i = 0; str[i] != '\0'; i++)
    {
        len++;
    }
    return len;
}
