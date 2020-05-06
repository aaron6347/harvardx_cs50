#include <stdio.h>
#include <cs50.h>

int main(void)
{   
    bool right = false;
    int height;
    int place = 1;
    // do while
    do
    {   
        // get input
        height = get_int("Height : ");
        // input validation
        if (height > 0 && height < 9)
        {
            right = true;
        }
            
    }
    while (right == false);
    // for 
    for (int i = 0; i < height; i ++)
    {
        // front block
        for (int j = 0; j < height; j ++)
        {
            if (height - j <= place)
            {
                printf("#");
            }
            else
            {
                printf(" ");
            }
        }
        // print middle 2 space
        printf("  ");
        // behind block
        for (int j = 0; j < place; j ++)
        {
            printf("#");
        }
        // go newline
        printf("\n");
        place++;
    }
}