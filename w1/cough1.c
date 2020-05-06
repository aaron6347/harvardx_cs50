#include <stdio.h>

void cough(int n);

int main(void){
    int n =get_int("n: \n");
    cough(n);
}

void cough(int n ){
    for (int i=0; i<n; i++)
        printf("cough\n");
}