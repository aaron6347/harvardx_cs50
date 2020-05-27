#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    string s = get_string("s: ");
    // string t = s;
    // t[0] = toupper(t[0]);
    printf("%s\n", s);
    // printf("%s\n", t);
    
    char *u = malloc(strlen(s)+1);
    // for (int i = 0, n = strlen(s)+1; i < n; i++)
    // {
    //     u[i] = s[i];
    // }
    
    strcpy(u, s);
    
    u[0] = toupper(u[0]);
    printf("%s\n", u);
    free(u);
}