#include<stdio.h>
int array[100];
int main()
{
    for(int i=0;i<50;i++)
    {
        array[i]=i;
        printf("%d",array[i]);
    }
    // for(int i=0;i<100;i++)
    // {
    //     printf("%d",array[i]);
    // }
    return 0;
}