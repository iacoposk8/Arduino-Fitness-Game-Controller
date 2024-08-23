
#include <MPU6050_tockn.h>
#include <Wire.h>

MPU6050 mpu6050(Wire);

long timer = 0;

void setup() {
  Serial.begin(38400);
  Serial.println("Wire");
  Wire.begin();
  Serial.println("mpu6050");
  mpu6050.begin();
  Serial.println("calcGyroOffsets");
  mpu6050.calcGyroOffsets(true);
  Serial.println("Setup Finish");
}

void loop() {
  mpu6050.update();

  //if(millis() - timer > 1000){

    String buf;
    buf += F("{");

    buf += F("\"temp\": ");
    buf += String(mpu6050.getTemp());
    buf += F(",");

    buf += F("\"accX\": ");
    buf += String(mpu6050.getAccX());
    buf += F(",");

    buf += F("\"accY\": ");
    buf += String(mpu6050.getAccY());
    buf += F(",");

    buf += F("\"accZ\": ");
    buf += String(mpu6050.getAccZ());
    buf += F(",");

    buf += F("\"gyroX\": ");
    buf += String(mpu6050.getGyroX());
    buf += F(",");

    buf += F("\"gyroY\": ");
    buf += String(mpu6050.getGyroY());
    buf += F(",");

    buf += F("\"gyroZ\": ");
    buf += String(mpu6050.getGyroZ());
    buf += F(",");

    buf += F("\"accAngleX\": ");
    buf += String(mpu6050.getAccAngleX());
    buf += F(",");

    buf += F("\"accAngleY\": ");
    buf += String(mpu6050.getAccAngleY());
    buf += F(",");

    buf += F("\"gyroAngleX\": ");
    buf += String(mpu6050.getGyroAngleX());
    buf += F(",");

    buf += F("\"gyroAngleY\": ");
    buf += String(mpu6050.getGyroAngleY());
    buf += F(",");

    buf += F("\"gyroAngleZ\": ");
    buf += String(mpu6050.getGyroAngleZ());
    buf += F(",");

    buf += F("\"angleX\": ");
    buf += String(mpu6050.getAngleX());
    buf += F(",");

    buf += F("\"angleY\": ");
    buf += String(mpu6050.getAngleY());
    buf += F(",");

    buf += F("\"angleZ\": ");
    buf += String(mpu6050.getAngleZ());
    //buf += F(",");

    buf += F("}");


    Serial.print(buf);
    Serial.println("");

    //timer = millis();
    
    /*Serial.println("=======================================================");
    Serial.print("temp : ");Serial.println(mpu6050.getTemp());
    Serial.print("accX : ");Serial.print(mpu6050.getAccX());
    Serial.print("\taccY : ");Serial.print(mpu6050.getAccY());
    Serial.print("\taccZ : ");Serial.println(mpu6050.getAccZ());
  
    Serial.print("gyroX : ");Serial.print(mpu6050.getGyroX());
    Serial.print("\tgyroY : ");Serial.print(mpu6050.getGyroY());
    Serial.print("\tgyroZ : ");Serial.println(mpu6050.getGyroZ());
  
    Serial.print("accAngleX : ");Serial.print(mpu6050.getAccAngleX());
    Serial.print("\taccAngleY : ");Serial.println(mpu6050.getAccAngleY());
  
    Serial.print("gyroAngleX : ");Serial.print(mpu6050.getGyroAngleX());
    Serial.print("\tgyroAngleY : ");Serial.print(mpu6050.getGyroAngleY());
    Serial.print("\tgyroAngleZ : ");Serial.println(mpu6050.getGyroAngleZ());
    
    Serial.print("angleX : ");Serial.print(mpu6050.getAngleX());
    Serial.print("\tangleY : ");Serial.print(mpu6050.getAngleY());
    Serial.print("\tangleZ : ");Serial.println(mpu6050.getAngleZ());
    Serial.println("=======================================================\n");
    timer = millis();*/
    
  //}

}
