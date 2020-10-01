#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 
#include <arpa/inet.h>
#include <unistd.h>


struct sockaddr_in dest_addr;
struct sockaddr_in source_addr;
char rx_buffer[5000];		// buffer to store data from client
char tx_buffer[5000];	

void closeSocket(int sock)
{
    close(sock);
    return;
}

int main()
{   printf("Started");
    int sock;
    int csock;
    source_addr.sin_family = AF_INET;
    source_addr.sin_addr.s_addr = INADDR_ANY;
    source_addr.sin_port = htons(3333);
    int clilen = sizeof(dest_addr);
    sock = socket(AF_INET, SOCK_STREAM, 0);
    bind(sock, (struct sockaddr *)&source_addr , sizeof(source_addr));
    
    listen(sock , 3);
    int c=0;
    while (1)
    {
        csock = accept(sock, (struct sockaddr *)&dest_addr, &clilen);

            while(recv(csock,&rx_buffer,sizeof(rx_buffer),0)>0)
            {
            char b[7]="";
            if(c==0){
             char d[7]="@(4,7)@";
             strcpy(b,d);
            c++;
            }
            else if(c==1){
             char d[7]="@(1,8)@";
             strcpy(b,d);
            }
            write(csock,b, sizeof(b));
            printf("Sent and received");
            }
        closeSocket(csock);
    }
    closeSocket(sock);
    printf("bye");
    return 0;
}