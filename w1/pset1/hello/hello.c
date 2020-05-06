#include <stdio.h>
#include <cs50.h>

int main(void)
{   
    // get name
    string name = get_string("What's is your name :D ?\n");
    // print the name with hello
    printf("hello, %s\n", name);
}