#include <stdio.h>
#include <cs50.h>
int main(void)
{
    //creating variable and asking user for his or her name
    string name = get_string("What's you name? ");
    //printing hello, with a placeholder for strings
    printf("hello, %s!\n", name);
}