#include <cs50.h>
#include <stdio.h>
#include <math.h>

int sentence_count(string text, int len);
int length(string text);
int letter_count(string text, int len);
bool isLetter(char letter);
int word_count(string text, int len);

int main(void)
{
    // Prompt the user for text
    string text = get_string("Text: ");

    // calcualte length of text
    int len = length(text);

    // Count the number of letters, words and sentences
    int letters = letter_count(text, len);
    int words = word_count(text, len);
    int sentences = sentence_count(text, len);

    // Computer the Coleman-Liau index
    float l = ((float) (letters * 100)) / words;
    float s = ((float) (sentences * 100)) / words;
    int index = round(0.0588 * l - 0.296 * s - 15.8);

    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
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

int letter_count(string text, int len)
{
    int letters = 0;
    for (int i = 0; i < len; i++)
    {
        if (isLetter(text[i]))
        {
            letters++;
        }
    }
    return letters;
}

bool isLetter(char letter)
{
    if ((letter >= 'a' && letter <= 'z') || (letter >= 'A' && letter <= 'Z'))
    {
        return true;
    }
    return false;
}

int word_count(string text, int len)
{
    int words = 0;
    int letters = false;
    for (int i = 0; i < len; i++)
    {
        if (letters == false && isLetter(text[i]))
        {
            letters = true;
        }
        else if (text[i] == '.' && letters == true)
        {
            words++;
            letters = false;
        }
        else if (text[i] == ' ' && letters == true)
        {
            words++;
            letters = false;
        }
    }
    return words;
}

int sentence_count(string text, int len)
{
    int sentences = 0;
    int letters = false;
    for (int i = 0; i < len; i++)
    {
        if (letters == false && isLetter(text[i]))
        {
            letters = true;
        }
        else if (text[i] == '.' && letters == true)
        {
            sentences++;
            letters = false;
        }
    }
    return sentences;
}
