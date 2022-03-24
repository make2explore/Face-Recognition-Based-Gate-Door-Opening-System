// ---------------------------------- make2explore.com----------------------------------------------------//
// Tutorial          - Raspberry Pi and EM-18 RFID Reader Interfacing
// Created By        - info@make2explore.com
// Version - 1.0
// Last Modified     - 07/02/2022 15:00:00 @admin
// Software          - C/C++, CodeBlocks IDE, Standard C/C++ Libraries
// Hardware          - Raspberry Pi 4 model B, FTDI Serial Adaptor Module, EM-18 RFID Reader, Level Converter
// Sensors Used      - EM-18 RFID Reader
// Source Repo       - github.com/make2explore
// -------------------------------------------------------------------------------------------------------//

#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <wiringPi.h>
#include <wiringSerial.h>


int sp;
int count1=0,count2=0,count3=0;
char ch;
char rfid[13];
int i=0;


int wiringPi_init(void);
int serialbegin(int);
void setup(void);
int get_card(void);


int wiringPi_init()
{
  if (wiringPiSetup () == -1)                                   /* initializes wiringPi setup */
  {
    fprintf (stdout, "Unable to start wiringPi: %s\n", strerror (errno));
    return 1;
  }
  return 0;
}

int serialbegin(int baud)
{
  if ((sp = serialOpen ("/dev/ttyAMA0",baud)) < 0)
  {
    fprintf (stderr, "Unable to open serial device: %s\n", strerror (errno));
    return 1;
  }
  return 0;
}

void setup()
{
  wiringPi_init();
  serialbegin(9600);
  delay(1000);
}

int get_card()
{
   i=0;
   while(i<12)
   {
     while(serialDataAvail(sp))
     {
       ch = serialGetchar(sp);
       rfid[i] = ch;
       fflush(stdout);
       i++;
     }
   }
  rfid[i]='\0';
  return 0;
}

int main()
{
  setup();
  while(1)
  {
    printf("\nPlace the RFID card on Reader ...\n");
    printf("\n");
    get_card();
    printf("RFID No : ");
    printf(rfid);
    printf("\n");
    delay(200);
    if(strncmp(rfid,"0900963100AE",12)==0)
    {
      count1++;
      printf("Hello Student 0\n");
    }
    else if(strncmp(rfid,"88001964699C",12)==0)
    {
      count2++;
      printf("Hello Student 1\n");
    }
    else if(strncmp(rfid,"880013E5235D",12)==0)
    {
      count2++;
      printf("Hello Student 2\n");
    }
    else if(strncmp(rfid,"880013E5225C",12)==0)
    {
      count2++;
      printf("Hello Student 3\n");
    }
    else if(strncmp(rfid,"880019646A9F",12)==0)
    {
      count2++;
      printf("Hello Student 4\n");
    }
    else
    {
      printf("Invalid Card\n");
    }
  }
  return 0;
}
