/*
 * Team Id: 2177
 * Author List: Nilendu
 * Filename: esp32.c
 * Theme: Rapid Rescuer
 * Functions: wifi_init_softap() , wifi_init_softap() , app_main()
 * Global Variables: *TAG
 */ 

#include <stdio.h>
#include <string.h>
#include <sys/param.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "esp_system.h"
#include "esp_wifi.h"
#include "esp_event_loop.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "tcpip_adapter.h"

#include "lwip/err.h"
#include "lwip/sockets.h"
#include "lwip/sys.h"
#include <lwip/netdb.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 
#include <arpa/inet.h>




#include "driver/uart.h"
#include "driver/gpio.h"

#define ECHO_TEST_TXD  (GPIO_NUM_32)            // Connected to AVR Rx-0
#define ECHO_TEST_RXD  (GPIO_NUM_33)            // Connected to AVR Tx-0
#define ECHO_TEST_RTS  (UART_PIN_NO_CHANGE)
#define ECHO_TEST_CTS  (UART_PIN_NO_CHANGE)

#define BUF_SIZE (1024)




#define PORT 3333				// Port address for socket communication
#define RX_BUFFER_SIZE 128

static const char *TAG = "ESP32";
static EventGroupHandle_t s_wifi_event_group;
/*
 * Function Name:esp_err_t event_handler
 * Input: Takes the values to check the esp wifi connection
 * Output: Give output as ESP_32 if everything is ok 
 * Logic: checks all connections
 * Example Call: esp_err_t event_handler(ctx,event1)
*/ 
 
static esp_err_t event_handler(void *ctx, system_event_t *event)
{
    switch(event->event_id) {
    case SYSTEM_EVENT_AP_STACONNECTED:
        ESP_LOGI(TAG, "station:"MACSTR" join, AID=%d",
                 MAC2STR(event->event_info.sta_connected.mac),
                 event->event_info.sta_connected.aid);
        break;
    case SYSTEM_EVENT_AP_STADISCONNECTED:
        ESP_LOGI(TAG, "station:"MACSTR"leave, AID=%d",
                 MAC2STR(event->event_info.sta_disconnected.mac),
                 event->event_info.sta_disconnected.aid);
        break;
    default:
        break;
    }
    return ESP_OK;
}

/*
 * Function Name:wifi_init_softap
 * Input: _
 * Output: _ 
 * Logic: Function to initialize Wi-Fi at station
 * Example Call: wifi_init_softap()
*/ 
void wifi_init_softap() //my_wifi_config my_wifi
{
    s_wifi_event_group = xEventGroupCreate();

    tcpip_adapter_init();
    ESP_ERROR_CHECK(esp_event_loop_init(event_handler, NULL));

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));
    wifi_config_t wifi_config = {
        .ap = {
            .ssid="eYFi-Wireless-Serial",
            .password="eyantra123",
            .ssid_len = 0,
            .channel = 6,
            .authmode = WIFI_AUTH_OPEN, //WIFI_AUTH_WPA_WPA2_PSK, //WIFI_AUTH_OPEN
            .ssid_hidden = 0,
            .max_connection=4,
            .beacon_interval = 100
        },
    };

    printf(">>>>>>>> SSID: %s <<<<<<<<<\n", wifi_config.ap.ssid);
    printf(">>>>>>>> PASS: %s <<<<<<<<<\n", wifi_config.ap.password);

    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_AP));
    ESP_ERROR_CHECK(esp_wifi_set_config(ESP_IF_WIFI_AP, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());
}


void app_main()
{

	ESP_ERROR_CHECK(nvs_flash_init());
	ESP_ERROR_CHECK(esp_event_loop_create_default());
	wifi_init_softap();

	char rx_buffer[RX_BUFFER_SIZE];     // buffer to store data from client
	char ipv4_addr_str[128];            // buffer to store IPv4 addresses as string
	char ipv4_addr_str_client[128];     // buffer to store IPv4 addresses as string
	int addr_family;
	int ip_protocol;

	char *some_addr;



   // ESP_ERROR_CHECK(nvs_flash_init());
   // ESP_ERROR_CHECK(esp_event_loop_create_default());

    uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE
    };
    uart_param_config(UART_NUM_1, &uart_config);
    uart_set_pin(UART_NUM_1, ECHO_TEST_TXD, ECHO_TEST_RXD, ECHO_TEST_RTS, ECHO_TEST_CTS);
    uart_driver_install(UART_NUM_1, BUF_SIZE * 2, 0, 0, NULL, 0);

    // data_uart:Configure a temporary buffer for the incoming data
    uint8_t *data_uart = (uint8_t *) malloc(BUF_SIZE);
v   //len_uart:data of uart communication between esp and atmega2560
    	int len_uart = 0;
    //count:variable for timeout
        unsigned int count = 0;
    //ack_buffer:string for sending to python 
        char ack_buffer[100];





	while (1) {

		struct sockaddr_in dest_addr;
		dest_addr.sin_addr.s_addr = htonl(INADDR_ANY);
		dest_addr.sin_family = AF_INET;
		dest_addr.sin_port = htons(PORT);
		addr_family = AF_INET;
		ip_protocol = IPPROTO_IP;
		
		inet_ntop( AF_INET, &dest_addr.sin_addr, ipv4_addr_str, INET_ADDRSTRLEN );
		//printf("[DEBUG] Self IP = %s\n", ipv4_addr_str);


		int listen_sock = socket(addr_family, SOCK_STREAM, ip_protocol);
		if (listen_sock < 0) {
			//printf("[ERROR] Unable to create socket. ERROR %d\n", listen_sock);
			break;
		}
		//printf("[DEBUG] Socket created\n");

		int flag = 1;
		setsockopt(listen_sock, SOL_SOCKET, SO_REUSEADDR, &flag, sizeof(flag));

		int err = bind(listen_sock, (struct sockaddr *)&dest_addr, sizeof(dest_addr));
		if (err != 0) {
			//printf("[ERROR] Socket unable to bind. ERROR %d\n", err);
			break;
		}

		//printf("[DEBUG] Socket bound, port %d\n", PORT);

		err = listen(listen_sock, 1);
		if (err != 0) {
			//printf("[ERROR] Error occurred during listen. ERROR %d\n", err);
			break;
		}

		//printf("[DEBUG] Socket listening\n");

		struct sockaddr_in6 source_addr; // Can store both IPv4 or IPv6
		uint addr_len = sizeof(source_addr);
		//the code below tries an initial connection with esp
		int sock = accept(listen_sock, (struct sockaddr *)&source_addr, &addr_len);
		if (sock < 0) {
			//printf("[ERROR] Error occurred during listen. ERROR %d\n", sock);
			break;
		}
		printf("[DEBUG] Socket accepted\n");

		while (1) {
			//len:length of the variable received from socket
			//recv function gets the string from socket and stores it in rx_buffer
			int len = recv(sock, rx_buffer, sizeof(rx_buffer) - 1, 0);
			printf("from soc:%s",rx_buffer);
			// Error occurred during receiving
			if (len < 0) {
				//printf("[ERROR] Receive failed. ERROR %d\n", len);
				break;
			}
			
			// Connection closed
			else if (len == 0) {
				//ESP_LOGI(TAG, "Connection closed");
				//printf("[DEBUG] Connection closed\n");
				break;
			}
			
			// Data received
			//after receiving data the esp communicates the data to the atmega 
			else {
				
				sprintf(ack_buffer, rx_buffer);
	        	ack_buffer[strlen(ack_buffer)] = NULL;
				printf("\n");
				printf("from python lenght: %d",strlen(ack_buffer));
	       		uart_write_bytes(UART_NUM_1, (const char *) ack_buffer, strlen(ack_buffer));
				//vTaskDelay(100);
                len_uart = uart_read_bytes(UART_NUM_1, data_uart, BUF_SIZE, 20 / portTICK_RATE_MS);
                data_uart[len_uart] = 0;
				printf("\nrecv from atmega....\n");
				printf("from arduino : %s",(char*)data_uart);
				sprintf(ack_buffer, (char*)data_uart);
                while (ack_buffer[0]== NULL)
                {
					free(data_uart);
			//data_uart is deleted and again delclared to prevent previous data from lingering on
					uint8_t *data_uart = (uint8_t *) malloc(BUF_SIZE);
                    printf("Waiting......");
                    len_uart = uart_read_bytes(UART_NUM_1, data_uart, BUF_SIZE, 20 / portTICK_RATE_MS);
                    data_uart[len_uart] = NULL;
					printf("got data %s",(char*)data_uart);
					sprintf(ack_buffer, (char*)data_uart);
					
                }
                
		//the if statement checks whether the data send to python is less than 128 bits
		//it also checks that if the len_uart variable has some value or not
                if(len_uart > 0 && len_uart<128){
                    sprintf(rx_buffer, (char*) data_uart);
					//printf(len_uart);
					//printf(rx_buffer);
                    len=(strlen((char*)data_uart));
                }
				//the string is sent to the python via the socket communication
				if (source_addr.sin6_family == PF_INET) {
					inet_ntop(AF_INET, &(source_addr.sin6_addr.s6_addr), ipv4_addr_str_client, INET_ADDRSTRLEN);

				} else if (source_addr.sin6_family == PF_INET6) {
					inet_ntop(AF_INET6, &(source_addr.sin6_addr.s6_addr), ipv4_addr_str_client, INET6_ADDRSTRLEN);
				}

				rx_buffer[len] = 0; // Add NULL to the string
				
				//printf("________________\n");
				//printf("[DEBUG] Received from Python Script: %s\n", rx_buffer);
				//send function sends the string rx_buffer to python
				int err = send(sock, rx_buffer, len, 0);
				if (err < 0) {
					//printf("[ERROR] Error occurred during sending. ERROR %d\n", err);
					break;
				} else {
					printf("\nsent to python\n");
					//printf("[DEBUG] Sending to Python Script: %s\n", rx_buffer);
					//printf("_______________\n");

				}
			}
		}

		if (sock != -1) {
			// Shutting down socket 
			shutdown(sock, 0);
			close(sock);

			shutdown(listen_sock,0);
			close(listen_sock);
			vTaskDelay(5); // Required for FreeRTOS on ESP32
		}
	}

	return 0;

}
