/*
GRMI_module.h - Library for GRMI_module.
Created by Juan S. Cely, Junio, 2017. GRMI CAR (UPM-CSIC).
*/
#ifndef GRMI_module_h
#define GRMI_module_h
/// Header files
#if (ARDUINO >= 100)
 #include "Arduino.h"
#else
 #include "WProgram.h"
#endif
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_BMP085_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_10DOF.h>
#include <Servo.h>

/// Define Variables
#define SSerialTxControl 30   // RS485 Direction control
#define SSerialRxControl 31
#define RS485Transmit    HIGH
#define RS485Receive     LOW
#define LEDTest          24

/// Class Define
class GRMI_module
{
	public: 
		GRMI_module(int, int, int); 
		void begin(int*);
		void GetRPYAngles(void);
		void GetCompass(void);
		void GetPressure(void);
		void SetRefPosMotor(int, int);
		void SetRefVelMotor(int, int);
		void SetKControlMotor(double);
		void SetDControlMotor(double);
		void RS485send(void);
		int* RS485received(int);
		void update(void);
		static void calculate(void);
		void SetPinsMotor(int*);
		double module_acceleration[3];
		double module_gyro[3];
		double module_angles[3];
		double module_magnetic[3];
		int module_pressure;
		double module_altitude;
		double module_orientation;
		double module_temperature;
		int initial_pos[3];
		int initial_vel[4];
		double RefPosMotor[3]={0,0,0};
		double RefVelMotor[4]={0,0,0,0};
		double KControlMotor;
		double DControlMotor;
		int motores_pins[4]={9,10,11,12};
		int ID_dir;
	private:
		void initServos(void);
		int _mode;
		int _dt;
		int _Num_motors;
};

#endif
