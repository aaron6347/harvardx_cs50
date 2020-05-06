#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

string checktype(long);

int main(void){
    bool right=false;
    do{
        long num=get_long("Number: ");
        string type=checktype(num);
        printf("\n%s\n",type);
        if (strcmp(type,"INVALID")!=0)
            right=true;
    }while(right==false);
    
    
}


string checktype(long num){
    char str[256];
    sprintf(str, "%li", num);
    int lenght=strlen(str);
    int prefix=num/pow(10, lenght-2);
    printf("\n%i %i", prefix, lenght);
    if (lenght==15 && (prefix==34 || prefix ==37))   
        return "AMEX";
    else if(lenght==16 && (prefix>50 && prefix <56))
        return "MASTERCARD";
    else if ((lenght==13 || lenght ==16) && prefix>=40)
        return "VISA";
    else
        return "INVALID";
}