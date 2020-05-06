#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    bool right = false;
    float change2;
    int change;
    int count = 0;
    // do while
    do
    {
        // take input
        change2 = get_float("Change owed: ");
        // change it to int
        change = round(change2 * 100);
        // validation of input
        if (change > 0)
        {
            right = true;
        }
    }
    while (right == false);
    
    // while 
    while (change > 0)
    {   
        // greedy with 25
        if (change >= 25)
        {
            change -= 25;
        }
        // greedy with 10
        else if (change >= 10)
        {
            change -= 10 ;
        } 
        // greedy with 5
        else if (change >= 5)
        {
            change -= 5 ;
        }
        // greedy with 1
        else if (change >= 1)
        {
            change -= 1;
        }
        // increment answer
        count++;
    }
    // print answer
    printf("%i\n", count);
    
}
