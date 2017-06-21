/* Library using example 
 * Set the module
 * Important: Have installed Adafruit Library
 * By: Juan S. Cely G.
 * GRMI - Research Group
 * June-2017
 */
#include <Wire.h> // Import the i2c main library
#include <GRMI_module.h> // Import GRMI library

GRMI_module modulito(101, 0, 30); // Define object with parameters ID, operation mode and sample time
int initial_val[3]={0,0,0}; // Initial Values 3 size to position, 4 size to velocity

void setup() {
  Serial.begin(9600);
  modulito.begin(initial_val); // Inicialization with initial parameter 
}

void loop() {
  modulito.update();  // Always in the loop, always!
  // To access to the object parameters check the documentation
  Serial.println("---");
  Serial.print("RPY: "); Serial.print(modulito.module_angles[0]); Serial.print(";"); Serial.print(modulito.module_angles[1]); Serial.print(";"); Serial.println(modulito.module_angles[2]);
  Serial.print("Mag: "); Serial.print(modulito.module_magnetic[0]); Serial.print(";"); Serial.print(modulito.module_magnetic[1]); Serial.print(";"); Serial.println(modulito.module_magnetic[2]);
  Serial.print("Presion: "); Serial.println(modulito.module_pressure);
  Serial.print("Altitud: "); Serial.println(modulito.module_altitude);
  Serial.print("Temperatura: "); Serial.println(modulito.module_temperature);
  Serial.println("");
}
