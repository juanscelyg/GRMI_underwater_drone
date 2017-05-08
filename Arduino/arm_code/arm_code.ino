/*
  Vida y mente de Luke

  Molesta la comunicacion, toca mejorar el protocolo y la forma de comunicacion, estoy estresado

  Elaboro: Juan Cely
  Fecha: 03/02/2017
*/
/////////////////////////////////////
///Librerias y archivos cabecera
#include <Servo.h>
//////////////////////////////////////
/// Direccion de contacto
#define mydir 101
//
/////////////////////////////////////
/// Definicion de variables y funciones
#define motor_1 9
#define motor_2 10
#define motor_3 11
#define SSerialRX        50  //Serial Receive pin
#define SSerialTX        51  //Serial Transmit pin
#define SSerialTxControl 30   //RS485 Direction control
#define SSerialRxControl 31
#define RS485Transmit    HIGH
#define RS485Receive     LOW
#define Pin13LED         13
#define LEDTest          24
#define ref_peligro      5    //Esto es la distancia en cm para detectar peligro
int dt = 40;
//
/////////////////////////////////////
/// Variables de la captura Serial
const double constante_conversion = 3.8461;
//
/////////////////////////////////////
/// Objetos
Servo Motor_1;
Servo Motor_2;
Servo Motor_3;
//
/////////////////////////////////////
/// Parametros objeto
int pos_ant_gripper = 180; // griper 180 muneca 90 codo 0 brazo 0
int pos_ant_muneca = 90;
int pos_ant_codo = 0;
int pos_ant_hombro = 0;
//
/////////////////////////////////////
/// Definicion de funciones
void avanzar(int, int);
void girar(int, int);
void enviar_rs485(String);
//
/////////////////////////////////////
void setup() {
  /// Inicializar Serial
  Serial.begin(9600);
  Serial2.begin(9600);
  /// Iniciar valores 485
  pinMode(Pin13LED, OUTPUT);
  pinMode(LEDTest, OUTPUT);
  pinMode(SSerialTxControl, OUTPUT);
  pinMode(SSerialRxControl, OUTPUT);
  digitalWrite(SSerialTxControl, RS485Receive);  // Init Transceiver
  digitalWrite(SSerialRxControl, RS485Receive);
  digitalWrite(13, LOW);
}

void loop() {
  //Copy input data to output
  if (Serial2.available() > 1) {
    String in_string = Serial2.readStringUntil(',');   // Read the byte
    int indice = in_string.lastIndexOf(',');
    String inString = in_string.substring(indice + 1);
    if (inString.length() > 3) {
      digitalWrite(LEDTest, HIGH);   
      delay(10);
      String stringone = inString.substring(0, 3);
      String stringtwo = inString.substring(3, 4);
      String stringtre = inString.substring(4, 7);
      String stringcua = inString.substring(7, 10);
      int variable = stringone.toInt();
      int variable2 = stringtwo.toInt();
      int variable3 = stringtre.toInt();
      int variable4 = stringcua.toInt();
      Serial.println("---");
      //    Serial.println(in_string);
      Serial.println(inString);
      Serial.println(variable);
      Serial.println(variable2);
      Serial.println(variable3);
      Serial.println(variable4);
      /// Variable
      if (variable == mydir) {
        digitalWrite(Pin13LED, HIGH);  // Show activity
        switch (variable2) {
          case 5:
            avanzar(variable3, variable4);
            break;
          case 6:
            girar(variable3, variable4);
            break;
        }
        digitalWrite(Pin13LED, LOW);  // Show activity
        digitalWrite(LEDTest, LOW);
      }
    }
  }
}

void enviar_rs485(String string_envio) {
  digitalWrite(SSerialTxControl, RS485Transmit);  // Enable RS485 Transmit
  digitalWrite(SSerialRxControl, RS485Transmit);
  Serial2.print(string_envio); // Send the byte back
  Serial2.flush();
  delay(10);
  digitalWrite(SSerialTxControl, RS485Receive);  // Disable RS485 Transmit
  digitalWrite(SSerialRxControl, RS485Receive);
}

void avanzar(int vel, int dir) {
  if (dir == 1) {
    analogWrite(motor_2, -vel);
    analogWrite(motor_3, vel);
  }
  if (dir == 0) {
    analogWrite(motor_2, vel);
    analogWrite(motor_3, -vel);
  }
}

void girar(int vel, int dir) {
  if (dir == 1) {
    analogWrite(motor_1, vel);
    analogWrite(motor_2, vel);
    analogWrite(motor_3, vel);
  }
  if (dir == 0) {
    analogWrite(motor_1, -vel);
    analogWrite(motor_2, -vel);
    analogWrite(motor_3, -vel);
  }
}

