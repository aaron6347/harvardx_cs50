#include <cs50.h>
#include <stdio.h>

void draw(int height);

int main(void)
{
    int height = get_int("Height: ");
    
    draw(height);
}

void draw(int height)
{
    if (height == 0)
    {
        return;
    }
    draw(height-1);
    for (int i = 0; i < height; i++)
    {
        printf("#");
    }
    printf("\n");
}