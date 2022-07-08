#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Prompt user for name
    string name = get_string("What is your name?\n");
    //Print user's name like Hi Name!
    printf("Hi %s!\n", name);
}