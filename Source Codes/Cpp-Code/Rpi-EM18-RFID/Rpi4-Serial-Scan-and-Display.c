// ---------------------------------- make2explore.com----------------------------------------------------//
// Tutorial          - Raspberry Pi Serial Port UART (Serial Read)
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

int main ()
{
  int serial_port ;
  char dat;
  if ((serial_port = serialOpen ("/dev/ttyAMA0", 9600)) < 0)	/* open serial port */
  {
    fprintf (stderr, "Unable to open serial device: %s\n", strerror (errno)) ;
    return 1 ;
  }

  if (wiringPiSetup () == -1)					/* initializes wiringPi setup */
  {
    fprintf (stdout, "Unable to start wiringPi: %s\n", strerror (errno)) ;
    return 1 ;
  }

  while(1){

	if(serialDataAvail (serial_port) )
	{
        dat = serialGetchar (serial_port);		/* receive character serially*/
        printf ("%c", dat) ;
        fflush (stdout) ;
        serialPutchar(serial_port, dat);		/* transmit character serially on port */
    }
}

}
