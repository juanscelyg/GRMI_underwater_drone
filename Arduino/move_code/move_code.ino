/*
  Vida y mente de Luke

  Molesta la comunicacion, toca mejorar el protocolo y la forma de comunicacion, estoy estresado

  Elaboro: Juan Cely
  Fecha: 21/03/2017
*/
/////////////////////////////////////
///Librerias y archivos cabecera
#include <Servo.h>

//////////////////////////////////////
/// Direccion de contacto
#define mydir 102
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
int pos = 0;
//
/////////////////////////////////////
/// Variables de la captura Serial
const double constante_conversion = 3.8461;
//
/////////////////////////////////////
/// Objetos
Servo gripper;
Servo muneca;
Servo codo;
Servo hombro;
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
void mover_gripper(int);
void mover_muneca(int);
void mover_codo(int);
void mover_hombro(int);
int girar(int);
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
  digitalWrite(Pin13LED, LOW);
  /// Iniciar servo gripper
  gripper.attach(4);
  gripper.write(pos_ant_gripper);
  /// Iniciar servo muneca
  muneca.attach(5);
  muneca.write(pos_ant_muneca);
  /// Iniciar servo codo
  codo.attach(6);
  codo.write(pos_ant_codo);
  //  /// Iniciar servo hombro
  hombro.attach(9);
  hombro.write(pos_ant_hombro);
}

void loop() {
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
          case 1:
            Serial.println("Gripper");
            if (variable3 == 1)
              mover_gripper(110);
            if (variable3 == 0)
              mover_gripper(180);
            break;
          case 2:
            Serial.println("Muneca");
            mover_muneca(variable3);
            break;
          case 3:
            Serial.println("Codo");
            mover_codo(variable3);
            break;
          case 4:
            Serial.println("Hombro");
            mover_hombro(variable3);
            break;
        }
        digitalWrite(Pin13LED, LOW);  // Show activity
        digitalWrite(LEDTest, LOW);
      }
    }
  }
}

void mover_gripper(int i) {
  if (i > pos_ant_gripper) {
    while (i > pos_ant_gripper) {
      gripper.write(pos_ant_gripper);
      pos_ant_gripper++;
      delay(dt);
    }
  }
  else if (i < pos_ant_gripper) {
    while (i < pos_ant_gripper) {
      gripper.write(pos_ant_gripper);
      pos_ant_gripper--;
      delay(dt);
    }
  }
  pos_ant_gripper = i;
}

void mover_muneca(int i) {
  if (i > pos_ant_muneca) {
    while (i > pos_ant_muneca) {
      muneca.write(pos_ant_muneca);
      pos_ant_muneca++;
      delay(dt);
    }
  }
  else if (i < pos_ant_muneca) {
    while (i < pos_ant_muneca) {
      muneca.write(pos_ant_muneca);
      pos_ant_muneca--;
      delay(dt);
    }
  }
  pos_ant_muneca = i;
}

void mover_codo(int i) {
  if (i > pos_ant_codo) {
    while (i > pos_ant_codo) {
      codo.write(pos_ant_codo);
      pos_ant_codo++;
      delay(dt);
    }
  }
  else if (i < pos_ant_codo) {
    while (i < pos_ant_codo) {
      codo.write(pos_ant_codo);
      pos_ant_codo--;
      delay(dt);
    }
  }
  pos_ant_codo = i;
}

void mover_hombro(int i) {
  if (i > pos_ant_hombro) {
    while (i > pos_ant_hombro) {
      hombro.write(pos_ant_hombro);
      pos_ant_hombro++;
      delay(dt);
    }
  }
  else if (i < pos_ant_hombro) {
    while (i < pos_ant_hombro) {
      hombro.write(pos_ant_hombro);
      pos_ant_hombro--;
      delay(dt);
    }
  }
  pos_ant_hombro = i;
}
