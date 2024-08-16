#include <cs50.h>
#include <stdio.h>

string cipher(string text, string key);
bool isValid(string key);
int length(string text);

int main(int argc, string argv[])
{
    // ensure key is given
    if (argc != 2)
    {
        printf("Usage : ./substitution key\n");
        return 1;
    }

    //ensure key is valid
    string key = argv[1];
    if (length(key) != 26 || isValid(key) == false)
    {
        printf("Key must contain 26 characters\n");
        return 1;
    }

    string plaintext = get_string("plaintext: ");
    printf("ciphertext: %s\n", cipher(plaintext, key));
}

bool isValid(string key)
{
    int alphabets[26];
    for (int i = 0; i < 26; i++)
    {
        if (key[i] >= 'a' && key[i] <= 'z')
        {
            for (int j = 0; j < i; j++)
            {
                if (alphabets[j] == key[i])
                {
                    return false;
                }
            }
            alphabets[i] = key[i];
        }
        if (key[i] >= 'A' && key[i] <= 'Z')
        {
            for (int j = 0; j < i; j++)
            {
                if (alphabets[j] == key[i])
                {
                    return false;
                }
            }
            alphabets[i] = key[i];
        }
        else
        {
            return false;
        }
    }
    return true;
}

int length(string text)
{
    int len = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        len++;
    }
    return len;
}

string cipher(string text, string key)
{
    for (int i = 0, len = length(text); i < len; i++)
    {
        if (text[i] >= 'a' && text[i] <= 'z')
        {
            text[i] = key[text[i]-97];
        }
        else if (text[i] >= 'A' && text[i] <= 'Z')
        {
            text[i] = key[text[i]-65];
        }
    }
    return text;
}
