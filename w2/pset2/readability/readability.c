#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    // get input
    string s = get_string("Text: ");
    // get length of string with strlen from string.h
    int n = strlen(s);
    // declare variables
    int L = 0;
    int W = 0;
    int S = 0;
    // find letter, word, sentence
    // for loop count letter, word, sentence
    for (int i = 0; i < n; i++)
    {
        // if character is alphabet
        if (isalpha(s[i]))
        {
            L++;
        }
        // if character is space means prefix is a complete word (assumption of no >1 spaces in a row and start or trail space)
        else if (isspace(s[i]))
        {
            W++;
        }
        // if character is . or !  or ? means prefix is a complete sentence
        else if (s[i] == '.' || s[i] == '!' || s[i] == '?')
        {
            S++;
        }
    }
    // since assumption of no >1 spaces in a row and start or trail space, the last character will be . and prefix is the last word
    W++;
    // printf("\n%i letter(s)", L);
    // printf("\n%i word(s)", W);
    // printf("\n%i sentence(s)", S);
    // find index
    // formula
    int index = round(0.0588 * L * 100 / W - 0.296 * S * 100 / W - 15.8);
    // print grade result
    // if index is less than 1
    if (index < 1)
    {
        printf("\nBefore Grade 1\n");
    }
    // if index is more than 16
    else if (index > 16)
    {
        printf("\nGrade 16+\n");
    }
    // if index is between includion of 1 to 16
    else
    {
        printf("\nGrade %i\n", index);
    }
}
