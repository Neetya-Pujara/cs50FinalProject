#include <cs50.h>
#include <ctype.h>
#include <stdio.h>

int calculate(string word, int letters[]);
int length(string str);
string strtoupper(string str);

int main(void)
{
    // input and score initialization
    int letter_scores[] = {1, 3, 3, 2,  1, 4, 2, 4, 1, 8, 5, 1, 3,
                           1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
    string word1 = strtoupper(get_string("Player 1: "));
    string word2 = strtoupper(get_string("Player 2: "));

    // calculate scores
    int score1 = calculate(word1, letter_scores);
    int score2 = calculate(word2, letter_scores);

    // compare scores
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
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

int calculate(string word, int letters[])
{
    int score = 0;
    for (int i = 0, len = length(word); i < len; i++)
    {
        if (word[i] >= 'A' && word[i] <= 'Z')
        {
            score += letters[word[i] - 65];
        }
    }
    return score;
}

string strtoupper(string str)
{
    for (int i = 0, len = length(str); i < len; i++)
    {
        str[i] = toupper(str[i]);
    }
    return str;
}
