#include<stdio.h>
#include<string.h>

char line_data[1000];
FILE *input_fp;
int k;
int main()
{ 
    //printf("hello");
    //printf("\n");
    char *input_file_name = "obtest.txt";
    input_fp = fopen(input_file_name, "r");
    if (input_fp == NULL){
		printf("Could not open file %s\n",input_file_name);
		return 1;
	}
    int c=0;
    int  i=0;
	int k;
    char digi[10];
	char send[1000]="    ";
	char points[50][50];
	int openb[50];
	int closeb[50];
    char rx_buffer1[1000]="2|alfnalehnfluhaeuofha";
    char tx_buffer[1000];
   // printf("%c",rx_buffer1[0]);
    //printf("\n");
    while(c<7)
    {
        //printf("%d ",c);
            //printf("\n");
	fgets(line_data, 1000, input_fp);
    digi[c]=line_data[0];
    c++;
    }

    for(i=0;i<10;i++)
    {
     if(rx_buffer1[0]==digi[i])
     {
     //printf("%d",i);
     k=i;
     //printf("%d",k);
     }
    }

    int m=0;
    rewind(input_fp);
    while(m<7)
    {
	fgets(line_data, 10000, input_fp);
    if(m==k)
    {
      //printf("%s",line_data);
        strcpy(send,line_data);
    }
    m++;
    }
	int o=0;
	int cl=0;
	for(i=0;i<30;i++)
	{ 
        char cha=send[i];
        //printf("%c",cha);
        
		if(cha=='(')
		{
         //printf("%d\n",i);
         openb[o]=i;
         //printf("%d\n",openb[o]);
		 o++;
         
		}
		if(cha==')')
		{
         closeb[cl]=i;
         //printf("%d\n",closeb[cl]);
		 cl++;
		}
	}
    //printf("%d\n",o);
    //  for(i=0;i<o;i++)
    // {
    // printf("%d",openb[i]);
    // }
    // for(i=0;i<o;i++)
    // {
    // printf("%d",closeb[i]);
    // }
	 for(i=0;i<o;i++)
	{  
        int z=openb[i];
        //printf("%d\n",z);
        int w=closeb[i];
        //printf("%d\n",w);
        int h=0;
		for(int j=z;j<w+1;j++)
		{   
            //printf("%d",j);
		points[i][h]=send[j];
        //printf("%c",points[i][h]);
        h++;
		}
        printf("\n");
	}
    strcpy(tx_buffer,points[1]);
    //printf("%s\n",tx_buffer);
	char a[5000]="@";
	strcat(tx_buffer,a);
    //printf("%s\n",tx_buffer);
    char tempe[5000];
    strcpy(tempe,tx_buffer);
    //printf("%s\n",tempe);
    strcat(a,tempe);
    //printf("%s\n",a);
    strcpy(tx_buffer,a);
    printf("%s\n",tx_buffer);

    
    
    //printf("%s",points[0]);
     return 0;
}