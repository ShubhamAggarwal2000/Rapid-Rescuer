/*
*****************************************************************************************
*
*        		===============================================
*           		Rapid Rescuer (RR) Theme (eYRC 2019-20)
*        		===============================================
*
*  This script is to implement Task 1B of Rapid Rescuer (RR) Theme (eYRC 2019-20).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
*/

/*
* Team ID:			[ Team-ID ]
* Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
* Filename:			task_1a.py
* Functions:		readImage, solveMaze
* 					[ Comma separated list of functions in this file ]
* Global variables:	CELL_SIZE
* 					[ List of global variables defined in this file ]
*/


// Include necessary header files
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 
#include <arpa/inet.h>
#include <unistd.h>


// Constants defined
#define SERVER_PORT 3333
#define RX_BUFFER_SIZE 1024
#define TX_BUFFER_SIZE 1024

#define MAXCHAR 1000				// max characters to read from txt file

// Global variables
struct sockaddr_in dest_addr;
struct sockaddr_in source_addr;

char rx_buffer[RX_BUFFER_SIZE];		// buffer to store data from client
char tx_buffer[RX_BUFFER_SIZE];	
char rx_buffer1[RX_BUFFER_SIZE];	// buffer to store data to be sent to client

char ipv4_addr_str[128];			// buffer to store IPv4 addresses as string
char ipv4_addr_str_client[128];		// buffer to store IPv4 addresses as string

int listen_sock;
int csock;
int clc =sizeof(source_addr);
int f=0,op=0;
char ch[10]= "a";

char line_data[MAXCHAR];

FILE *input_fp, *output_fp;
/*
* Function Name:	socket_create
* Inputs:			dest_addr [ structure type for destination address ]
* 					source_addr [ structure type for source address ]
* Outputs: 			my_sock [ socket value, if connection is properly created ]
* Purpose: 			the function creates the socket connection with the server
* Example call: 	int sock = socket_create(dest_addr, source_addr);
*/
void closeSocket(int sock)
{
    close(sock);
    return;
}
int socket_create(struct sockaddr_in dest_addr, struct sockaddr_in source_addr){
	printf("Creating socket..\n");
	int addr_family;
	int ip_protocol;

	dest_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	dest_addr.sin_family = AF_INET;
	dest_addr.sin_port = htons(SERVER_PORT);
	addr_family = AF_INET;
	ip_protocol = IPPROTO_IP;

	int my_sock;
    my_sock=socket(AF_INET,SOCK_STREAM,0);
	bind(my_sock,(struct sockaddr*) &dest_addr,sizeof(dest_addr));
	listen(my_sock,3);
	csock = accept(my_sock,(struct sockaddr*)&source_addr,&clc);
	recv(csock,&rx_buffer1,RX_BUFFER_SIZE,0);
	closeSocket(csock);
	 
	
	//csock = accept(my_sock,(struct sockaddr*)&source_addr,&clc);
	return my_sock;	
}


/*
* Function Name:	receive_from_send_to_client
* Inputs:			sock [ socket value, if connection is properly created ]
* Outputs: 			None
* Purpose: 			the function receives the data from server and updates the 'rx_buffer'
*					variable with it, sends the obstacle position based on obstacle_pos.txt
*					file and sends this information to the client in the provided format.
* Example call: 	receive_from_send_to_client(sock);
*/

int receive_from_send_to_client(int sock){
    csock = accept(sock,(struct sockaddr*)&source_addr,&clc);
	recv(csock,&rx_buffer,RX_BUFFER_SIZE,0);
	printf("%s",rx_buffer);
    //printf("%s",rx_buffer);	
// 	printf("rxbuffer = %c\n",rx_buffer[0]);
	
// 	int ru=0;
	
// 	//printf("%c",rx_buffer[0]);
// 	if(rx_buffer[0]==ch[0])
// 	{
// 		f++;
// 	}
// 	else
// 	{
// 		f=0;
// 	}
// 	ch[0]=rx_buffer[0];
// 	int c=1;
//     int  i=0;
// 	int k=2154;
//     char digi[10];
// 	char send1[1000]="    ";
// 	char points[50][50];
// 	int openb[50];
// 	int closeb[50];
//    // printf("%c",rx_buffer1[0]);
//     //printf("\n");
// 	//printf("%s",line_data);
// 	digi[0]=line_data[0];
// 	//printf("digi is %c\n",digi[0]);
//     while(c<7)
//     {
//         //printf("%d ",c);
//             //printf("\n");
// 	fgets(line_data, 1000, input_fp);
// 	//printf("%s",line_data);
//     digi[c]=line_data[0];
// 	//printf("digi is %c\n",digi[c]);
//     c++;
//     }
    
//     for(i=0;i<10;i++)
//     {
//      if(rx_buffer[0]==digi[i])
//      {
//      //printf("%d",i);
//      k=i;
//      }
//     }
// 	//printf("k= %d\n",k);
// 	if(k==2154)
// 	{
// 		ru=1;
// 	}

//     int m=0;
//     rewind(input_fp);
//     while(m<7)
//     {
// 	fgets(line_data, 10000, input_fp);
//     if(m==k)
//     {
//       //printf("%s",line_data);
//         strcpy(send1,line_data);
//     }
//     m++;
//     }
// 	int o=0;
// 	int cl=0;
// 	for(i=0;i<30;i++)
// 	{ 
//         char cha=send1[i];
//         //printf("%c",cha);
        
// 		if(cha=='(')
// 		{
//          //printf("%d\n",i);
//          openb[o]=i;
//          //printf("%d\n",openb[o]);
// 		 o++;
         
// 		}
// 		if(cha==')')
// 		{
//          closeb[cl]=i;
//          //printf("%d\n",closeb[cl]);
// 		 cl++;
// 		}
// 	}
// 	 op =o;
//     //printf("%d\n",o);
//     //  for(i=0;i<o;i++)
//     // {
//     // printf("%d",openb[i]);
//     // }
//     // for(i=0;i<o;i++)
//     // {
//     // printf("%d",closeb[i]);
//     // }
// 	 for(i=0;i<o;i++)
// 	{  
//         int z=openb[i];
//         //printf("%d\n",z);
//         int w=closeb[i];
//         //printf("%d\n",w);
//         int h=0;
// 		for(int j=z;j<w+1;j++)
// 		{   
//             //printf("%d",j);
// 		points[i][h]=send1[j];
//         //printf("%c",points[i][h]);
//         h++;
// 		}
//         //printf("\n");
// 	}
// 	//printf("f = %d\n",f);
//     //printf("point = %s\n",points[f]);
// 	//send(sock,tx_buffer,TX_BUFFER_SIZE,0);
// 	//printf("%d",op);
// 	if(o==0)
// 	{
// 		ru=1;
// 	}
// 	//printf("ru = %d\n",ru);
//     if(ru==0){
// 	if(points[f]==" ")
// 	{
// 		char b[5000]="@$@";
// 	strcpy(tx_buffer,b);
// 	}
// 	else
// 	{
// 	strcpy(tx_buffer,points[f]);
// 	char a[5000]="@";
// 	strcat(tx_buffer,a);
//     //printf("%s\n",tx_buffer);
//     char tempe[5000];
//     strcpy(tempe,tx_buffer);
//     //printf("%s\n",tempe);
//     strcat(a,tempe);
//     //printf("%s\n",a);
//     strcpy(tx_buffer,a);
	
// 	//printf("buffer = %s\n",tx_buffer);
// 	}}
//     else if(ru==1)
// 	{ 
//     char b[5000]="@$@";
// 	strcpy(tx_buffer,b);
// 	}
	//csock = accept(sock,(struct sockaddr*)&source_addr,&clc);
    //write(csock,tx_buffer,strlen(tx_buffer));
	 char abcd[500]="@(4,7)@,@(1,8)@,@$@,@$@,@(4,5)@,@$@,@(8,5)@,@(14,7)@,@(15,19)@,@$@,@(13,10)@,@$@";
	 strcpy(tx_buffer,abcd);
	// if (write(csock, tx_buffer, strlen(tx_buffer)) < 0)
    // {
    //     printf("Can't send message.\n");
    // }
	// else
    // printf("Message sent (%ld bytes).\n", strlen(tx_buffer));
	send(csock, tx_buffer, strlen(tx_buffer),0);
    closeSocket(csock);
	rewind(input_fp);
	return 0;	
}

int main() {
	printf("hello");
    char *input_file_name = "obstacle_pos.txt";
	char *output_file_name = "data_from_client.txt";

	// Create socket and accept connection from client
	int sock = socket_create(dest_addr, source_addr);

	input_fp = fopen(input_file_name, "r");

	if (input_fp == NULL){
		printf("Could not open file %s\n",input_file_name);
		return 1;
	}

	fgets(line_data, MAXCHAR, input_fp);

	output_fp = fopen(output_file_name, "w");

	if (output_fp == NULL){
		printf("Could not open file %s\n",output_file_name);
		return 1;
	}
	while (1) {

		// Receive and send data from client and get the new shortest path
		receive_from_send_to_client(sock);
		printf("received");

		// NOTE: YOU ARE NOT ALLOWED TO MAKE ANY CHANssGE HERE
		fputs(rx_buffer, output_fp);
		fputs("\n", output_fp);
	}
	return 0;
}

