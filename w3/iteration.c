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
    for (int i = 0; i <= height; i++)
    {
        for (int j = 0; j < i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}