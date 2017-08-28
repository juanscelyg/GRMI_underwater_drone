/*
GRMI_module.h - Library for GRMI_module.
Created by Juan S. Cely, Junio, 2017. GRMI CAR (UPM-CSIC).
*/

#if (ARDUINO >= 100)
 #include "Arduino.h"
#else
 #include "WProgram.h"
#endif
/// Headers Files
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_BMP085_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_10DOF.h>
#include "Timer.h"
#include <Servo.h>
#include <GRMI_module.h>

/// Code byAdafruit
/* Assign a unique ID to the sensors Code by Adafruit */
Adafruit_10DOF                	dof   	= Adafruit_10DOF();
Adafruit_LSM303_Accel_Unified 	accel 	= Adafruit_LSM303_Accel_Unified(30301);
Adafruit_L3GD20_Unified 		gyro 	= Adafruit_L3GD20_Unified(20);
Adafruit_LSM303_Mag_Unified   	mag   	= Adafruit_LSM303_Mag_Unified(30302);
Adafruit_BMP085_Unified       	bmp   	= Adafruit_BMP085_Unified(18001);

/* Update this with the correct SLP for accurate altitude measurements Code by Adafruit */
float seaLevelPressure = SENSORS_PRESSURE_SEALEVELHPA;
///End Code

/// Define Objects and Variables
Timer t;
Servo motor1;
Servo motor2;
Servo motor3;
Servo motor4;
int modo=0;
int dt_;
double p_module_acceleration[3];
double p_module_gyro[3];
double p_module_angles[3];
double p_module_magnetic[3];
double p_RefPosMotor[3];
double p_module_pressure;
double p_module_altitude;
double p_module_orientation;
double p_module_temperature;
double last_error_signal[3]={0,0,0};
double K_control=0.9525;
double D_control=0.4892;
int vector_pins[4];

void initSensors()
{
  if(!accel.begin())
  {
    Serial.println(F("No LSM303 detected."));
    while(1);
  }
  if(!gyro.begin())
  {
    Serial.println("No L3GD20 detected.");
    while(1);
  }
  if(!mag.begin())
  {
    Serial.println("No LSM303 detected.");
    while(1);
  }
  if(!bmp.begin())
  {
    Serial.println("No BMP180 detected.");
    while(1);
  }
}
/// End Code

int ControlPosMotor(int ID_motor, double ref_motor, double valor, double error_1, int d_t)
{
	double error=ref_motor-valor;
	double c=(K_control*error+(D_control*1000/d_t)*error-(D_control*1000/d_t)*error_1)*500/12; // 500 i the change the value on PWM module and 12 is the working voltage 
	if (c<-500) // Saturation
	{ 
		c=-500;
	}
	if (c>500)
	{
		c=500;
	} 
	last_error_signal[ID_motor-1]=error;
	return int(c)+1500;
}

/// Constructor
GRMI_module::GRMI_module(int dir, int mode, int dt)
{
   ID_dir = dir;
   _mode = mode;
   modo=_mode;
   _dt = dt;
   dt_=dt;
   KControlMotor=K_control;
   DControlMotor=D_control;
   memcpy(&vector_pins,&motores_pins,sizeof(motores_pins));
}

/// Public Methods
void GRMI_module::begin(int* initial_values)
{	
	for(int i=0;i<_Num_motors;i++){
		if (_mode==0){
			initial_pos[i]=initial_values[i];
			SetRefPosMotor(i, initial_pos[i]);
		}
		else if (_mode==1){
			initial_vel[i]=initial_values[i];
			SetRefVelMotor(i, initial_vel[i]);
		}
	}
	gyro.enableAutoRange(true);
	initServos();
	initSensors();
	int tickEvent = t.every(_dt,calculate);  
}

void GRMI_module::initServos()
{
	motor1.attach(motores_pins[0]);
	motor1.writeMicroseconds(1500); // send "stop" signal to ESC.
	motor2.attach(motores_pins[1]);
	motor2.writeMicroseconds(1500); // send "stop" signal to ESC.
	motor3.attach(motores_pins[2]);
	motor3.writeMicroseconds(1500); // send "stop" signal to ESC.
	motor4.attach(motores_pins[3]);
	motor4.writeMicroseconds(1500); // send "stop" signal to ESC.
	delay(1000); // delay to allow the ESC to recognize the stopped signal
}

void GRMI_module::GetAcceleration()
{
	module_acceleration[0]=p_module_acceleration[0];
	module_acceleration[1]=p_module_acceleration[1];
	module_acceleration[2]=p_module_acceleration[2];
}

void GRMI_module::GetRPYAngles()
{
	module_angles[0]=p_module_angles[0];
	module_angles[1]=p_module_angles[1];
	module_angles[2]=p_module_angles[2];
}

void GRMI_module::GetCompass()
{
	module_magnetic[0]=p_module_magnetic[0];
	module_magnetic[1]=p_module_magnetic[1];
	module_magnetic[2]=p_module_magnetic[2];
}

void GRMI_module::GetPressure()
{
	module_pressure=p_module_pressure;
	module_altitude=p_module_altitude;
	module_temperature=p_module_temperature;
}

void GRMI_module::SetRefPosMotor(int motor, int value)
{
	RefPosMotor[motor-1]=value;
	p_RefPosMotor[motor-1]=value;
}

void GRMI_module::SetRefVelMotor(int motor, int value)
{
	RefVelMotor[motor-1]=value;
}

void GRMI_module::SetKControlMotor(double value)
{
	KControlMotor=value;
	K_control=value;
}

void GRMI_module::SetDControlMotor(double value)
{
	DControlMotor=value;
	D_control=value;
}

void GRMI_module::SetPinsMotor(int* pines)
{
	memcpy(&motores_pins,&pines,sizeof(pines));
	memcpy(&vector_pins,&pines,sizeof(pines));
}

void GRMI_module::RS485send()
{

}

int* GRMI_module::RS485received(int port)
{
	String in_string;
	if (port==1){
		in_string = Serial.readStringUntil(','); 
	}
	if (port==2){
		#if defined(__AVR_ATmega1280__) || defined(__AVR_ATmega2560__)
		in_string = Serial2.readStringUntil(','); 
		#endif
	}
	if (port==3){
		#if defined(__AVR_ATmega1280__) || defined(__AVR_ATmega2560__)
		in_string = Serial3.readStringUntil(','); 
		#endif
	}
	int indice = in_string.lastIndexOf(',');
	String inString = in_string.substring(indice + 1);
	int* pointer;
	int variable[4]={0,0,0,0};
	pointer=variable;
	if (inString.length() > 3) {
		digitalWrite(LEDTest, HIGH);   
		String stringone = inString.substring(0, 3);
		String stringtwo = inString.substring(3, 4);
		String stringtre = inString.substring(4, 7);
		String stringcua = inString.substring(7, 10);
		variable[0] = stringone.toInt();
		variable[1] = stringtwo.toInt();
		variable[2] = stringtre.toInt();
		variable[3] = stringcua.toInt();
	}
	if (variable[0]==ID_dir)
	{
		return pointer;
	}
	else{
		variable[0] = 0;
		variable[1] = 0;
		variable[2] = 0;
		variable[3] = 0;
		return pointer;
	}
}

void GRMI_module::calculate()
{
	sensors_event_t accel_event;
	sensors_event_t gyro_event; 
	sensors_event_t mag_event;
	sensors_event_t bmp_event;
	sensors_vec_t   orientation;
	
	/// accelerometer
	accel.getEvent(&accel_event);
	if (dof.accelGetOrientation(&accel_event, &orientation))
	{
		p_module_angles[0]=orientation.roll;
		p_module_angles[1]=orientation.pitch;  
	}
	p_module_acceleration[0]=accel_event.acceleration.x;
	p_module_acceleration[1]=accel_event.acceleration.y;
	p_module_acceleration[2]=accel_event.acceleration.z;
	
	/// Gyro
	gyro.getEvent(&gyro_event);
	p_module_gyro[0]=gyro_event.gyro.x;
	p_module_gyro[1]=gyro_event.gyro.y;
	p_module_gyro[2]=gyro_event.gyro.z;
	
	/// Magnetometer
	mag.getEvent(&mag_event);
	if (dof.magGetOrientation(SENSOR_AXIS_Z, &mag_event, &orientation))
	{
		p_module_angles[2]=orientation.heading;
	}
	p_module_magnetic[0]=mag_event.magnetic.x;
	p_module_magnetic[1]=mag_event.magnetic.y;
	p_module_magnetic[2]=mag_event.magnetic.z;

	/// Barometer
	bmp.getEvent(&bmp_event);
	if (bmp_event.pressure)
	{
		float temperature;
		bmp.getTemperature(&temperature);
		p_module_altitude=bmp.pressureToAltitude(seaLevelPressure,bmp_event.pressure,temperature);
		p_module_temperature=temperature;
		p_module_pressure=bmp_event.pressure;
	}
	if (modo==0){
		motor1.writeMicroseconds(ControlPosMotor(1,p_RefPosMotor[0], p_module_angles[0], last_error_signal[0], dt_));
		motor2.writeMicroseconds(ControlPosMotor(2,p_RefPosMotor[1], p_module_angles[1], last_error_signal[1], dt_));
		motor3.writeMicroseconds(ControlPosMotor(3,p_RefPosMotor[2], p_module_angles[2], last_error_signal[2], dt_));		
	}
	else if (modo==1){
		// Dont move, be quiet! 
		motor1.writeMicroseconds(1500);
		motor2.writeMicroseconds(1500);
		motor3.writeMicroseconds(1500);
		motor4.writeMicroseconds(1500);	
	}
}

void GRMI_module::update()
{
	t.update();
	GetAcceleration();
	GetRPYAngles();
	GetCompass();
	GetPressure();
}
