/*
 * Team Id: 2177
 * Author List:Gaurav Nagotanekar
 * Filename:robot-t5-atmega2560
 * Theme:Rapid Rescuer
 * Functions: init_led, led_redOn, led_redOFF led_redOn, led_redOFF led_redOn, led_redOFF motor_init 
 * timer15_init, movel,mover , error, ch_add, pid, init_devices , readings_tof,readings_lfa,recv_data, turn_left, turn_right, uturn, stop, go,
 * gain_path,gain_digit,check_heading,pid_line_white,pid_line_black,init_button
 * Global Variables: sensor1_newadress,sensor1_newadress,sensor1_newadress,sensor,default_motorspeed,one,f_send,temp,rx,val1,val2,val3,val11,val22,val33
 * ad1,ad2,ad3,lfa,rx_byte,i,k,lfav,kp,kd,od,motorspeed,er,prv_er,x,y,c,heading,path_length,x1,y1,opp,clp,temp,temp1,te,pl,l,m,v,path_number,firex,digits,yc,firezone,l1,m1,v1
 */
#define F_CPU 16000000
#include <stdio.h>
#include<string.h>
#include<stdlib.h>
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include "i2c.h"
#include "uart.h"
#include "VL53L0X.h"
#include "millis.h"
#include "mcp23017.h"
#define PIN_BUTTON		PE7	  // Macro for Pin Number of Switch
#define PIN_ML_0    PL3       // Macro for Pin Number of Motor1 pin1
#define PIN_ML_1	PB5       // Macro for Pin Number of Motor1 pin2
#define PIN_MR_0	PL5       // Macro for Pin Number of Motor2 pin1
#define PIN_MR_1	PB6       // Macro for Pin Number of Motor2 pin2
#define R_TOF   PA5           // Macro for Pin Number of right tof 
#define L_TOF   PA1			  // Macro for Pin Number of left tof 
#define F_TOF	PA3	          // Macro for Pin Number of front tof 
#define PIN_LED_RED		PH3	  // Macro for Pin Number of Red Led
#define PIN_LED_BLUE	PH4	  // Macro for Pin Number of Blue Led
#define PIN_LED_GREEN	PH5	  // Macro for Pin Number of Green Led
#define zero 0
int default_motorspeed=65;
uint8_t Sensor1_newAddress=44;
uint8_t Sensor2_newAddress=46;
uint8_t Sensor3_newAddress=48;
uint8_t Sensor[3];
uint8_t one=1;
unsigned char f_send[50],temp[50];
// for tof sensors//
uint16_t val1,val2,val3;
int val11,val22,val33;
uint8_t ad1,ad2,ad3,lfa;
char rx_byte;
int i=0,k=0,lfav;
char rx[1024],recv[1024],recvp[1024];
//////////////////// 

// for pid // 
int kp=8;
int kd=25;
int od=37;
int motorspeed;
int er=0;
int prv_er=0;
//////////// 

//int x[50][10],y[50][10],c[2];
int heading=0;
int path_length[10];
int n,x1,y1;
////////////////////////////////

// global variables for gaining path //
int opp[50],clp[50],k,x[50][50],y[50][50],c[2];
char temp1[200];
char te[10];
int pl[50];
int l=0,m=0,v=0;path_number=0;
// // // // // // // // // // // // // 

// global variables for gaining digits//
int firex[50],digits[50],yc[50];
int firezone,firezones[50];
int  l1=0,m1=0,v1=0;
// // // // // // // // // // // // //

void init_led(){
	DDRH    |= (1 << PIN_LED_RED) | (1 << PIN_LED_BLUE) | (1 << PIN_LED_GREEN);     // initialize the pins PIN_LED_RED,PIN_LED_BLUE,PIN_LED_GREEN of port H as output pins.
	DDRE &= ~(1 << PIN_BUTTON);
	PORTH   |= (1 << PIN_LED_RED) | (1 << PIN_LED_BLUE) | (1 << PIN_LED_GREEN);     // set the values that all the LEDs remains off initially
}
unsigned char button_read(void){
	unsigned char status = PINE >> PIN_BUTTON;	// Read PIN_BUTTON
	return status;
}
void led_redOn(void){
	PORTH &= ~(1 << PIN_LED_RED);		// Make PHPIN_LED_RED Low
}

void led_redOff(void){
	PORTH |= (1 << PIN_LED_RED);		// Make PHPIN_LED_RED High
}


void led_blueOn(void){
	PORTH &= ~(1 << PIN_LED_BLUE);		// Make PHPIN_LED_BLUE Low
}

void led_blueOff(void){
	PORTH |= (1 << PIN_LED_BLUE);		// Make PHPIN_LED_BLUE High
}
void led_greenOn(void){
	PORTH &= ~(1 << PIN_LED_GREEN);		// Make PHPIN_LED_GREEN Low
}

void led_greenOff(void){
	PORTH |= (1 << PIN_LED_GREEN);		// Make PHPIN_LED_GREEN High
}
void motor_init(void)
{
	DDRL    |= (1 << PIN_ML_0)  | (1 << PIN_MR_0);  
	DDRB    |=  (1 << PIN_ML_1) | (1 << PIN_MR_1);  
	PORTL   |= (1 << PIN_ML_0)  | (1 << PIN_MR_0);  
	PORTB   |= (1 << PIN_ML_1) | (1 << PIN_MR_1);   
	 
}
void timer15_init()
{
	 /*
▪ * Function Name:initialize timer 1 and timer 5
▪ * Input: void

▪ * Output:void 

▪ 

▪ *
in the function>
▪ * Example Call: timer15_init();
▪ */
	cli(); //disable all interrupts
	
	TCCR1B = 0x00;	//Stop
    TCCR5B = 0x00;	//Stop
	
	TCNT1H = 0xFF;	//Counter higher 8-bit value to which OCR5xH value is compared with
	TCNT1L = 0x00;	//Counter lower 8-bit value to which OCR5xH value is compared with
	
	OCR1AH = 0x00;	//Output compare register high value for Red Led
	OCR1AL = 0xFF;	//Output compare register low value for Red Led
	
	OCR1BH = 0x00;	//Output compare register high value for Blue Led
	OCR1BL = 0xFF;	//Output compare register low value for Blue Led

	OCR1CH = 0x00;	//Output compare register high value for Green Led
	OCR1CL = 0xFF;	//Output compare register low value for Green Led
    
    TCNT5H = 0xFF;	//Counter higher 8-bit value to which OCR5xH value is compared with
	TCNT5L = 0x00;	//Counter lower 8-bit value to which OCR5xH value is compared with
	
	OCR5AH = 0x00;	//Output compare register high value for Red Led
	OCR5AL = 0xFF;	//Output compare register low value for Red Led
	
	OCR5BH = 0x00;	//Output compare register high value for Blue Led
	OCR5BL = 0xFF;	//Output compare register low value for Blue Led

	OCR5CH = 0x00;	//Output compare register high value for Green Led
	OCR5CL = 0xFF;	//Output compare register low value for Green Led
	
	
	//  Clear OC4A, OC4B & OC4C on compare match (set output to low level)
	TCCR5A |= (1 << COM5A1) | (1 << COM5B1) | (1 << COM5C1);
	TCCR5A &= ~((1 << COM5A0) | (1 << COM5B0) | (1 << COM5C0));
    TCCR1A |= (1 << COM1A1) | (1 << COM1B1) | (1 << COM1C1);
	TCCR1A &= ~((1 << COM1A0) | (1 << COM1B0) | (1 << COM1C0));

	// FAST PWM 8-bit Mode
	TCCR5A |= (1 << WGM50);
	TCCR5A &= ~(1 << WGM51);
	TCCR5B |= (1 << WGM52);
    TCCR1A |= (1 << WGM10);
	TCCR1A &= ~(1 << WGM11);
	TCCR1B |= (1 << WGM12);
	
	// Set Prescalar to 64
	TCCR5B |= (1 << CS51) | (1 << CS50);
	TCCR5B &= ~(1 << CS52);
    TCCR1B |= (1 << CS11) | (1 << CS10);
	TCCR1B &= ~(1 << CS12);
	
	sei(); //re-enable interrupts
}
void movel (unsigned int left_speed_1, unsigned int left_speed_0){
	OCR5AL = 255 - (unsigned int)left_speed_0; 	// active low thats why subtracting by 255
    OCR1AL = 255 - (unsigned int)left_speed_1; 	
}
void mover (unsigned int right_speed_1, unsigned int right_speed_0){
	OCR5CL = 255 - (unsigned int)(right_speed_0);  // active low thats why subtracting by 255
	OCR1BL = 255 - (unsigned int)(right_speed_1);
}
int error(void)
{
/*
▪ * Function Name:error
▪ * Input: void
▪ * Output: returns the error of pid for avoiding wall
▪ * Logic:the distance of each sensor is taken and its difference with optimum distance of walls and robot is taken to give error
▪ * Example Call: error();
▪ */
    readings_tof();
    int erl=od-val11;//error left
    int err=od-val33;//error right
    er=(erl-err);//combined error ; positive means go right
	return er;
}
void ch_add()
{
	/*
▪ * Function Name:ch_add
▪ * Input: void
▪ * Output: changes the i2c address of  tof sensor
▪ * Logic:2 sensors are giving xshut high and address of 1 sensor is changed
▪ * Example Call: ch_add();
▪ */
	DDRA=0xFF;
	DDRA&=~(1 << L_TOF);
	_delay_ms(10);
	setAddress(0,Sensor1_newAddress);
	ad1= getAddress(0);
	_delay_ms(10);
	DDRA&=~(1 << F_TOF);
	setAddress(1,Sensor2_newAddress);
	 ad2= getAddress(1);
	_delay_ms(10);
	DDRA&=~(1 << R_TOF);
	setAddress(2,Sensor3_newAddress);
	_delay_ms(10);
	 ad3= getAddress(2);
}
void pid(void)
{
	/*
▪ * Function Name:pid
▪ * Input: void
▪ * Output: monitors motor speed for pid wall avoidance
▪ * Logic:the error is multipled with constants to monitor speed of motors
▪ * Example Call: pid();
▪ */
  er=error();
  er = (exp(er) - exp(-er))/ (exp(er) + exp(-er));
  motorspeed=kp*er+kd*(er-prv_er);
  prv_er=er;
  movel(default_motorspeed+motorspeed+2,0);
  mover(default_motorspeed-motorspeed,0);
}
void init_devices (void) {
	motor_init();
	timer15_init();
}
char uart0_readByte(void){

	uint16_t rx;
	uint8_t rx_status, rx_data;

	rx = uart0_getc();
	rx_status = (uint8_t)(rx >> 8);
	rx = rx << 8;
	rx_data = (uint8_t)(rx >> 8);

	if(rx_status == 0 && rx_data != 0){
		return rx_data;
	} else {
		return -1;
	}
} 
void readings_tof()
{/*
▪ * Function Name:readings_tof
▪ * Input: void
▪ * Output: returns the raw value of tof sensor in mm
▪ * Logic:the library VL53LOX had to be changed for doing so
▪ * Example Call: readings_tof();
▪ */
    //i2c_start(ad1);
	val1=readRangeContinuousMillimeters(0,0);
	 val11=(int)val1-40;
	//i2c_start(ad2);
	val2=readRangeContinuousMillimeters(1,0);
	 val22=(int)val2;	
	//i2c_start(ad3);
	val3=readRangeContinuousMillimeters(2,0);
	 val33=(int)val3-30;
	sprintf(f_send,"@{tof1:%d,tof2:%d,tof3:%d}@\n",val11,val22,val33);
}
void readings_lfa()
{
	/*
▪ * Function Name:readings_lfa
▪ * Input: void
▪ * Output: returns the raw readings of lfa sensor
▪ * Logic: the sensor array is  read.
▪ * Example Call: readings_lfa);
▪ */
	lfa=mcp23017_readpinsA(0);
	lfav=(int)lfa;
	sprintf(temp,"%d\n",lfav);
	uart0_puts(temp);
}
void recv_data()
{
	/*
▪ * Function Name:recv_data
▪ * Input: void
▪ * Output: returns data received from esp
▪ * Logic:
▪ * Example Call: recv_data();
▪ */
	while(1)
	{
	   rx_byte=uart0_readByte();
	   if(rx_byte != -1){
            rx[i]=rx_byte;
			i++;
			// uart0_putc(rx_byte);
			// uart0_puts("\n");
		}
		if( rx_byte == -1 && rx[0]!='*' )
		{
			// uart0_puts(rx);
			// uart0_puts("\n");
			strcpy(recv,rx);
			for(size_t i=0;i<sizeof rx;++i)
			{
			rx[i]=0;
			}
			rx[0]='*';
			i=0;
			k=0;
			break;
		}
	    _delay_ms(1);
	}
}
void turn_left()
{   readings_tof();
    int f=val22;
	int r=val33;
	while(-30>f-r || f-r>30)
	{
	 movel(0,90);
	 mover(90,0);
	 readings_tof();
	 r=val33;
	//  sprintf(temp,"%d\n",f-r);
	//  uart0_puts(temp);
	}
	movel(0,0);
	mover(0,0);
  if(heading==0)heading=3;
  else if(heading==2)heading=1;
  else if(heading==3)heading=2;
  else if(heading==1)heading=0;
}
void turn_right()
{   readings_tof();
    int f=val22;
	int r=val33;
	while(-30>f-r || f-r>30)
	{
	 mover(0,90);
	 movel(90,0);
	 readings_tof();
	 r=val33;
	//  sprintf(temp,"%d\n",f-r);
	//  uart0_puts(temp);
	}
	movel(0,0);
	mover(0,0);
  if(heading==0)heading=1;
  else if(heading==1)heading=2;
  else if(heading==2)heading=3;
  else if(heading==3)heading=0;
}
void uturn()
{
	turn_right();
	turn_right();
}
void stop()
{
	movel(0,0);
	mover(0,0);
}
void go(int x,int y)
{/*
▪ * Function Name:go
▪ * Input:  co ordinates of next block to go
▪ * Output: moves robot to respective co ordinate
▪ * Logic:checks the heading, if its correct it moves one block
▪ * Example Call: go();
▪ */
    if (x-c[0]==1)
	{
		if(heading==0)
		{
			turn_right();
		}
		else if(heading==3)
		{
			uturn();
		}
		else if(heading==2)
		{
			turn_left();
		}
 readings_lfa();	
    while(lfav<48)
	{
		readings_lfa();
		pid();
	}
	stop();
	}
	else if (x-c[0]==-1)
	{
		if(heading==0)
		{
			turn_left();
		}
		else if(heading==1)
		{
			uturn();
		}
		else if(heading==2)
		{
			turn_right();
		}
  readings_lfa();	
    while(lfav<48)
	{
		readings_lfa();
		pid();
	}
	stop();	
	}
	else if (x-c[0]==0)
	{
		if(y-c[1]==1)
		{
           if(heading==1)
		{
			turn_left();
		}
		else if(heading==2)
		{
			uturn();
		}
		else if(heading==3)
		{
			turn_right();
		}
	readings_lfa();	
    while(lfav<48)
	{
		readings_lfa();
		pid();
	}	
	stop();
		}
	else if(y-c[1]==-1)
		{
           if(heading==3)
		{
			turn_left();
		}
		else if(heading==0)
		{
			uturn();
		}
		else if(heading==1)
		{
			turn_right();
		}
		}
   readings_lfa();	
    while(lfav<48)
	{
		readings_lfa();
		pid();
	}
	stop();	
	}
}
void gain_path()
{ 
	/*
▪ * Function Name:gain_path
▪ * Input: void
▪ * Output: does string handeling and retunrs the path
▪ * Logic:
▪ * Example Call: gain_path();
▪ */
	v=0;
for(int t=0;t<strlen(recv);t++)
{
	if(recv[t]=='|'){te[v]=t; v++;}
} 
path_number=v-1;
for(int t=0;t<path_number;t++)
{l=0;m=0;
for(int k=te[t];k<te[t+1];k++)
  {
	  if (recv[k]=='(')
	  {
		opp[l]=k;
		l++;
	  }
	  else if (recv[k]==')')
	  {
		clp[m]=k;
		m++;
	  }
}
pl[t]=l;
for(k=0;k<l;k++)
{   
	
	x[t][k]=(int)recv[opp[k]+1]-'0';
}
for(k=0;k<m;k++)
{
	y[t][k]=(int)recv[clp[k]-1]-'0';
}		
}

// print  path //


// for(int j=0;j<path_number;j++)
// 	{
// 	sprintf(temp,"path %d : ",j);
// 	uart0_puts(temp);
// 	for(k=0;k<pl[j];k++)
// 	{
// 	sprintf(temp,"%d:(%d,%d)  ",k,x[j][k],y[j][k]);
// 	uart0_puts(temp);
// 	}
// 	uart0_puts("\n");
// 	}

}
void gain_digit()
{
	/*
▪ * Function Name:gain_digit
▪ * Input: void
▪ * Output: does string handeling and retunrs the digits recieved
▪ * Logic:
▪ * Example Call: gain_digit();
▪ */
   char op[10];
   char cl[10];
   char co[10];
   l1=0,m1=0,v1=0;
  for(k=0;k<strlen(recv);k++)
  {
	  if (recv[k]=='(')
	  {
		op[l1]=k;
	// 	sprintf(temp,"o %d\n ",op[l1]);
	// uart0_puts(temp); 
		l1++;
		
	  }
	  else if (recv[k]==')')
	  {
		cl[m1]=k;
	// 	sprintf(temp,"c %d\n ",cl[m1]);
	// uart0_puts(temp); 
		m1++;
	  }	 
	   else if (recv[k]==':')
	  {
		co[v1]=k;
		v1++;
	  }	 
  }
  for(int f=0;f<v1;f++)
   { 
	 
	 firex[f]= (int)(recv[op[f]+1]-'0');
	 yc[f]=(int)(recv[cl[f]-1]-'0');
   	 digits[f]=(int)recv[co[f]-1]-'0';	 
  }
  firezone=v1;

  // printing //
  
//   for(int f=0;f<v1;f++)
//    { 
// 	 sprintf(temp,"%d : (%d,%d)\n",digits[f],firex[f],yc[f]);
// 	 uart0_puts(temp);
//   }

  // // // // // 
}
void check_heading(int x,int y,int i,int j)
{
	/*
▪ * Function Name:check_heading
▪ * Input: void
▪ * Output: corrects the heading of the bot
▪ * Logic:
▪ * Example Call: check_heading();
▪ */
	if (x-i==1)
	{
		if(heading==0)
		{
			turn_right();
		}
		else if(heading==3)
		{
			uturn();
		}
		else if(heading==2)
		{
			turn_left();
		}
	}
	else if (x-i==-1)
	{
		if(heading==0)
		{
			turn_left();
		}
		else if(heading==1)
		{
			uturn();
		}
		else if(heading==2)
		{
			turn_right();
		}
	}
	else if (x-i==0)
	{
		if(y-j==1)
		{
           if(heading==1)
		{
			turn_left();
		}
		else if(heading==2)
		{
			uturn();
		}
		else if(heading==3)
		{
			turn_right();
		}
		}
	else if(y-j==-1)
		{
           if(heading==3)
		{
			turn_left();
		}
		else if(heading==0)
		{
			uturn();
		}
		else if(heading==1)
		{
			turn_right();
		}
		}
	}
}
void pid_line_white()
{ 	/*
▪ * Function Name:pid_line_white
▪ * Input: void
▪ * Output: makes the robot follow white line
▪ * Logic: takes the  lfa value, converts it into binary, multiplies it by array of[0,1000,2000,...,7000]
then takes average of value and substracts 3500 from it.
▪ * Example Call: pid_line_white();
▪ */
	int prv_err=0;
	while(1){
	readings_lfa();
	if(lfav==0||lfav==248)
	{
		break;
	}
	int err1=255-lfav;
	int err=24-err1;
	int kpl=10;
	int kdl=3;
	int ms=kpl*err+kdl*(err-prv_err);
	_delay_ms(100);
	movel(default_motorspeed + ms,0);
	mover(default_motorspeed-ms,0);
	prv_err=err;
}

}

void pid_line_black()
{ 
/*
▪ * Function Name:pid_line_black
▪ * Input: void
▪ * Output: makes the robot follow white line
▪ * Logic: takes the  lfa value, converts it into binary, multiplies it by array of[0,1000,2000,...,7000]
then takes average of value and substracts 3500 from it.
▪ * Example Call: pid_line_black();
▪ */
	int prv_err=0;
	while(1){
	readings_lfa();
	if(lfav==0||lfav==248)
	{
		break;
	}
	int err1=lfav;
	int err=24-err1;
	int kpl=10;
	int kdl=3;
	int ms=kpl*err+kdl*(err-prv_err);
	_delay_ms(100);
	movel(default_motorspeed + ms,0);
	mover(default_motorspeed-ms,0);
	prv_err=err;
}
}

void init_button(void){
	DDRE &= ~(1 << PIN_BUTTON);		// Make PIN_BUTTON input
	PORTE |= (1 << PIN_BUTTON);		// Turn on Internal Pull-Up resistor of PIN_BUTTON (Optional)
}

int main(void) {
	uart0_init(UART_BAUD_SELECT(9600, F_CPU));  //initialize uart0
	uart0_flush();
	// initialize buttons, leds , motors ,timers
	init_devices();
	init_led();
	i2c_init();
	init_button();
	ch_add();
	//uart0_puts("changed");
	initVL53L0X(0,1);
	initVL53L0X(1,1);
	initVL53L0X(2,1);
	//uart0_puts("INIT");
    mcp23017_init();
	mcp23017_setmodeA(MCP23017_BASEADDRESS,MCP23017_MODEINPUTALL);
	mcp23017_setmodeB(MCP23017_BASEADDRESS,MCP23017_MODEOUTPUTALL);
	mcp23017_writepinsB(MCP23017_BASEADDRESS,MCP23017_PINSTATEOFFALL);
	startContinuous(0,0);
	startContinuous(1,0);readings_lfa();
	startContinuous(2,0);
	rx[0]='*';
	c[0]=0;
    c[1]=0;
	int h=0;
	while(1)
	{recv_data();
	 recv_data(); 
	 gain_digit(); // receive digits
	 recv_data();
	 strcpy(recvp,recv);
	 while(recv[0]!="D")
	 {
	 recv_data();
	 strcat(recvp,recv);
	 }
	 strcpy(recv,recvp);
	 gain_path(); // receive path
	 while(button_read() != 1);
	 uart0_puts("@started@");
	 // go to firezone ////
	 for(int j=0;j<=firezone;j++)
	 {
	 for(int i=0;i<path_length[j];i++)
	 {
	 go(x[j][i],y[j][i]);
	 }
	 check_heading(firezones[2*j],firezones[2*j+1],x[path_length[j]-1],y[path_length[j]-1]);
	 sprintf(f_send,"@$|%d|(%d,%d)@",digits[j],firex[j],yc[j]);
	 uart0_puts(f_send);
     led_redOn();
	 _delay_ms(1000);
	 led_redOff(); 
	 c[0]=x[j][path_length[j]-1];
	 c[1]=y[j][path_length[j]-1];
	}
	/////////////////
	//turn_right();
	// move through line //
	movel(100,0);
	mover(100,0);
	_delay_ms(200);
	stop();
	pid_line_black();
	if(lfav==0)
	{
	movel(100,0);
	mover(100,0);
	_delay_ms(200);	
	stop();
	turn_left();
	}
	pid_line_black();
	if(lfav==248)
	{
	movel(100,0);
	mover(100,0);
	_delay_ms(200);	
	stop();
	turn_right();
	}
	movel(100,0);
	mover(100,0);
	_delay_ms(200);	
	stop();
	uart0_puts("@HA reached@");
	led_greenOn();
	_delay_ms(1000);
	led_greenOff();
	uturn();
	movel(100,0);
	mover(100,0);
	_delay_ms(200);	
	stop();
	turn_right();
	pid_line_black();
    if(error==24)
	{
	movel(100,0);
	mover(100,0);
	_delay_ms(200);	
	stop();	
	}
	turn_left();
	pid_line_white();
	if(error==231)
	{
	movel(100,0);
	mover(100,0);
	_delay_ms(200);	
	stop();	
	}
	turn_left();
	pid_line_black();
	if(lfav==248)
	{
	movel(100,0);
	mover(100,0);
	_delay_ms(200);	
	stop();
	turn_right();
	}
	movel(100,0);
	mover(100,0);
	_delay_ms(200);	
	stop();
	uart0_puts("@HB reached@");
	led_greenOn();
	_delay_ms(1000);
	led_greenOff();
	uturn();
	movel(100,0);
	mover(100,0);
	_delay_ms(200);	
	stop();
	turn_right();
	pid_line_black();
    if(error==24)
	{
	movel(100,0);
	mover(100,0);
	_delay_ms(200);	
	stop();	
	}
	turn_left();
	pid_line_white();
	if(lfav==248)
	{
	movel(100,0);
	mover(100,0);
	_delay_ms(200);	
	stop();
	turn_right();
	}
	movel(100,0);
	mover(100,0);
	_delay_ms(200);	
	stop();
	uart0_puts("@HC reached, Task accomplished!@");
	led_greenOn();
	_delay_ms(1000);
	led_greenOff();
	while(1);
	}
	return 0;	
} 