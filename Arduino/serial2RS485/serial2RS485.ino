#include <SoftwareSerial.h>
/*-----( Declare Constants and Pin Numbers )-----*/
#define SSerialRX        10  //Serial Receive pin
#define SSerialTX        11  //Serial Transmit pin
#define SSerialTxControl 2   //RS485 Direction control
#define SSerialRxControl 3
#define RS485Transmit    HIGH
#define RS485Receive     LOW
#define Pin13LED         13

SoftwareSerial RS485Serial(SSerialRX, SSerialTX); // RX, TX

void setup()
{
  // Start the built-in serial port, probably to Serial Monitor
  Serial.begin(9600);
  RS485Serial.begin(9600);   // set the data rate
  pinMode(Pin13LED, OUTPUT);
  pinMode(SSerialTxControl, OUTPUT);
  pinMode(SSerialRxControl, OUTPUT);
  digitalWrite(SSerialTxControl, RS485Receive);  // Init Transceiver
  digitalWrite(SSerialRxControl, RS485Receive);  // Init Transceiver
}

void loop()
{
  if (Serial.available() > 1)
  {
    digitalWrite(Pin13LED, HIGH);  // Show activity
    char inString = Serial.read();
    digitalWrite(SSerialTxControl, RS485Transmit);  // Enable RS485 Transmit
    digitalWrite(SSerialRxControl, RS485Transmit);
    RS485Serial.print(inString);          // Send byte to Remote Arduino
    RS485Serial.flush();
    delay(10);
    digitalWrite(SSerialTxControl, RS485Receive);  // Disable RS485 Transmit
    digitalWrite(SSerialRxControl, RS485Receive);
    digitalWrite(Pin13LED, LOW);  // Show activity
  }

  if (RS485Serial.available() > 1) //Look for data from other Arduino
  {
    digitalWrite(Pin13LED, HIGH);  // Show activity
    char outString = RS485Serial.read();
    Serial.println(outString);        // Show on Serial Monitor
    Serial.flush();
    delay(10);
    digitalWrite(Pin13LED, LOW);  // Show activity
  }

}
