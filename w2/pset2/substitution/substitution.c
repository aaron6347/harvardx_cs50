#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

//main with arguments
int main(int argc, string argv[])
{
    // if arguments aren't 2
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    // if the length of 2nd argument is not 26 length
    else if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    // 2nd argument's character checks

    //  use for check exactly once and further use in cipher
    int alpha_ascii_uppercase[26] = {};
    // check non-alphabet character
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        // if the 2nd argument contain non-alphabetic character
        if (!isalpha(argv[1][i]))
        {
            printf("Key must be alphabet characters.\n");
            return 1;
        }
        // if character is alphabet, take its ascii value of uppercase to further check each letter has exaclty once
        else
        {
            alpha_ascii_uppercase[i] = (int) toupper(argv[1][i]);
        }
    }

    // check each letter has exactly once
    for (int i = 0; i < 26; i++)
    {
        for (int j = 0; j < 26; j++)
        {
            // when not in same index, only do checking
            if (i != j)
            {
                // if exist same ascii value of uppercase (that means more than once)
                if (alpha_ascii_uppercase[i] == alpha_ascii_uppercase[j])
                {
                    printf("Key must be each unique alphabetic characters.\n");
                    return 1;
                }
            }
        }
    }

    // if no error in arguments
    // get input
    string s = get_string("plaintext: ");
    // to store ciphertext
    int n = strlen(s);
    int answer [n];
    for (int i = 0; i < n; i++)
    {
        // if character is alphabetic
        if (isalpha(s[i]))
        {
            // find its index to find cipher
            int find_pos = (int) toupper(s[i]) - 65;
            // if the character is lowercase then cipher it to lowercase
            if islower(s[i])
            {
                answer[i] = alpha_ascii_uppercase[find_pos] + 32;
            }
            // if the character is uppercase then cipher it to uppercase
            else
            {
                answer[i] = alpha_ascii_uppercase[find_pos];
            }
        }
        // if character is non-alphabetic
        else
        {
            answer[i] = (int) s[i];
        }
    }
    // display ciphertext
    printf("\nciphertext: ");
    // print all character of ciphertext
    for (int i = 0; i < n; i++)
    {
        printf("%c", (char) answer[i]);
    }
    printf("\n");
}
