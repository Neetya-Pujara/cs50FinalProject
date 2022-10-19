#include <stdio.h>
#include <cs50.h>
#include <strings.h>

int main (void)
{
    string word = "Hello";
    string user = get_string("Word : ");
    if (strcasecmp(word, user) == 0)
    {
        printf("Then why?!!!!!!!!\n");
    }
    else
    {
        printf("Say tolower and create your own method\n");
    }
}