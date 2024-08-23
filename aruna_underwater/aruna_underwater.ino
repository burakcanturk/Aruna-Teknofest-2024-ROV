#include <Servo.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <MPU6050_tockn.h>
#include <MadgwickAHRS.h>
#include <PID_v1.h>
#include <Base.h>

#define dis Serial1
#define rs485 Serial2

#define upper_right_front_esc_pin 16
#define upper_left_front_esc_pin 17
#define upper_right_back_esc_pin 18
#define upper_left_back_esc_pin 19
#define lower_right_front_esc_pin 20
#define lower_left_front_esc_pin 21
#define lower_right_back_esc_pin 22
#define lower_left_back_esc_pin 26

#define relay0_pin 13
#define relay1_pin 14
#define relay2_pin 15

#define dis_sw_pin 2

#define front_dis_mux 0
#define lower_dis_mux 1

#define ESC_MIN 1000
#define ESC_STOP 1500
#define ESC_MAX 2000

#define URF_VAL_ROW 0
#define ULF_VAL_ROW 1
#define URB_VAL_ROW 2
#define ULB_VAL_ROW 3
#define LRF_VAL_ROW 4
#define LLF_VAL_ROW 5
#define LRB_VAL_ROW 6
#define LLB_VAL_ROW 7
#define RELAY0_VAL_ROW 8
#define RELAY1_VAL_ROW 9
#define RELAY2_VAL_ROW 10
#define FILTER_RESET_ROW 11
#define GYRO_CALIB_ROW 12

#define DIS_FRONT_VAL_ROW 128
#define DIS_LOWER_VAL_ROW 129
#define GYRO_ROLL_VAL_ROW 130
#define GYRO_PITCH_VAL_ROW 131
#define GYRO_YAW_VAL_ROW 132
#define VOLTAGE_VAL_ROW 133
#define CURRENT_VAL_ROW 134
#define POWER_VAL_ROW 135

Servo upper_right_front_esc;
Servo upper_left_front_esc;
Servo upper_right_back_esc;
Servo upper_left_back_esc;
Servo lower_right_front_esc;
Servo lower_left_front_esc;
Servo lower_right_back_esc;
Servo lower_left_back_esc;

MPU6050 mpu6050(Wire);
Madgwick filter;

Base base;

byte val_row;

struct land_vals {
  uint16_t upper_right_front_val;
  uint16_t upper_left_front_val;
  uint16_t upper_right_back_val;
  uint16_t upper_left_back_val;
  uint16_t lower_right_front_val;
  uint16_t lower_left_front_val;
  uint16_t lower_right_back_val;
  uint16_t lower_left_back_val;
  bool relay0_val;
  bool relay1_val;
  bool relay2_val;
  bool filter_reset;
  bool gyro_calib;
} landVals;

struct underwater_vals {
  int16_t dis_front_val;
  int16_t dis_lower_val;
  float roll;
  float pitch;
  float yaw;
  float voltage;
  float current;
  float power;
} underwaterVals;

struct gyroVals {
  float ax;
  float ay;
  float az;
  float gx;
  float gy;
  float gz;
} gyro_vals;

int16_t getDis(int sira);
void readGyro();
float readRoll();
float readPitch();
float readYaw();

void sendSignalReceived() {
  //rs485.write('+');
}

void setup() {

  Serial.begin(115200);
  rs485.begin(9600);
  dis.begin(115200);

  pinMode(dis_sw_pin, OUTPUT);

  pinMode(relay0_pin, OUTPUT);
  pinMode(relay1_pin, OUTPUT);
  pinMode(relay2_pin, OUTPUT);

  digitalWrite(relay0_pin, HIGH);
  digitalWrite(relay1_pin, HIGH);
  digitalWrite(relay2_pin, HIGH);

  upper_right_front_esc.attach(upper_right_front_esc_pin, ESC_MIN, ESC_MAX);
  upper_left_front_esc.attach(upper_left_front_esc_pin, ESC_MIN, ESC_MAX);
  upper_right_back_esc.attach(upper_right_back_esc_pin, ESC_MIN, ESC_MAX);
  upper_left_back_esc.attach(upper_left_back_esc_pin, ESC_MIN, ESC_MAX);
  lower_right_front_esc.attach(lower_right_front_esc_pin, ESC_MIN, ESC_MAX);
  lower_left_front_esc.attach(lower_left_front_esc_pin, ESC_MIN, ESC_MAX);
  lower_right_back_esc.attach(lower_right_back_esc_pin, ESC_MIN, ESC_MAX);
  lower_left_back_esc.attach(lower_left_back_esc_pin, ESC_MIN, ESC_MAX);

  upper_right_front_esc.writeMicroseconds(ESC_STOP);
  upper_left_front_esc.writeMicroseconds(ESC_STOP);
  upper_right_back_esc.writeMicroseconds(ESC_STOP);
  upper_left_back_esc.writeMicroseconds(ESC_STOP);
  lower_right_front_esc.writeMicroseconds(ESC_STOP);
  lower_left_front_esc.writeMicroseconds(ESC_STOP);
  lower_right_back_esc.writeMicroseconds(ESC_STOP);
  lower_left_back_esc.writeMicroseconds(ESC_STOP);

  Wire.begin();
  mpu6050.begin();
  mpu6050.calcGyroOffsets(true);
  filter.begin(25);

  base.begin();
  base.currentOffset(-1.48);

  openDis(0);
  while (dis.available() > 0) dis.read();

  //delay(5000);

  openDis(0);
  while (dis.available() > 0) dis.read();

  Serial.println("System started.");
}

void loop() {

  if (rs485.available() > 0) {

    val_row = rs485.read();

    Serial.println(val_row);

    switch (val_row) {

      case URF_VAL_ROW:
        rs485.readBytes((uint8_t*)&landVals.upper_right_front_val, sizeof(landVals.upper_right_front_val));
        upper_right_front_esc.writeMicroseconds(landVals.upper_right_front_val);
        sendSignalReceived();
        break;

      case ULF_VAL_ROW:
        rs485.readBytes((uint8_t*)&landVals.upper_left_front_val, sizeof(landVals.upper_left_front_val));
        upper_left_front_esc.writeMicroseconds(landVals.upper_left_front_val);
        sendSignalReceived();
        break;

      case URB_VAL_ROW:
        rs485.readBytes((uint8_t*)&landVals.upper_right_back_val, sizeof(landVals.upper_right_back_val));
        upper_right_back_esc.writeMicroseconds(landVals.upper_right_back_val);
        sendSignalReceived();
        break;

      case ULB_VAL_ROW:
        rs485.readBytes((uint8_t*)&landVals.upper_left_back_val, sizeof(landVals.upper_left_back_val));
        upper_left_back_esc.writeMicroseconds(landVals.upper_left_back_val);
        sendSignalReceived();
        break;

      case LRF_VAL_ROW:
        rs485.readBytes((uint8_t*)&landVals.lower_right_front_val, sizeof(landVals.lower_right_front_val));
        lower_right_front_esc.writeMicroseconds(landVals.lower_right_front_val);
        sendSignalReceived();
        break;

      case LLF_VAL_ROW:
        rs485.readBytes((uint8_t*)&landVals.lower_left_front_val, sizeof(landVals.lower_left_front_val));
        lower_left_front_esc.writeMicroseconds(landVals.lower_left_front_val);
        sendSignalReceived();
        break;

      case LRB_VAL_ROW:
        rs485.readBytes((uint8_t*)&landVals.lower_right_back_val, sizeof(landVals.lower_right_back_val));
        lower_right_back_esc.writeMicroseconds(landVals.lower_right_back_val);
        sendSignalReceived();
        break;

      case LLB_VAL_ROW:
        rs485.readBytes((uint8_t*)&landVals.lower_left_back_val, sizeof(landVals.lower_left_back_val));
        lower_left_back_esc.writeMicroseconds(landVals.lower_left_back_val);
        sendSignalReceived();
        break;

      case RELAY0_VAL_ROW:
        rs485.readBytes((uint8_t*)&landVals.relay0_val, sizeof(landVals.relay0_val));
        digitalWrite(relay0_pin, not landVals.relay0_val);
        sendSignalReceived();
        break;

      case RELAY1_VAL_ROW:
        rs485.readBytes((uint8_t*)&landVals.relay1_val, sizeof(landVals.relay1_val));
        digitalWrite(relay1_pin, not landVals.relay1_val);
        sendSignalReceived();
        break;

      case RELAY2_VAL_ROW:
        rs485.readBytes((uint8_t*)&landVals.relay2_val, sizeof(landVals.relay2_val));
        digitalWrite(relay2_pin, not landVals.relay2_val);
        sendSignalReceived();
        break;

      case FILTER_RESET_ROW:
        rs485.readBytes((uint8_t*)&landVals.filter_reset, sizeof(landVals.filter_reset));
        if (landVals.filter_reset) filter = Madgwick();
        sendSignalReceived();
        break;

      case GYRO_CALIB_ROW:
        rs485.readBytes((uint8_t*)&landVals.gyro_calib, sizeof(landVals.gyro_calib));
        if (landVals.gyro_calib) mpu6050.calcGyroOffsets(true);
        sendSignalReceived();
        break;

      //-------------------------------------------------

      case DIS_FRONT_VAL_ROW:
        underwaterVals.dis_front_val = getDis(front_dis_mux);
        rs485.write((uint8_t*)&underwaterVals.dis_front_val, sizeof(underwaterVals.dis_front_val));
        break;

      case DIS_LOWER_VAL_ROW:
        underwaterVals.dis_lower_val = getDis(lower_dis_mux);
        rs485.write((uint8_t*)&underwaterVals.dis_lower_val, sizeof(underwaterVals.dis_lower_val));
        break;

      case GYRO_ROLL_VAL_ROW:
        underwaterVals.roll = readRoll();
        rs485.write((uint8_t*)&underwaterVals.roll, sizeof(underwaterVals.roll));
        break;

      case GYRO_PITCH_VAL_ROW:
        underwaterVals.pitch = readPitch();
        rs485.write((uint8_t*)&underwaterVals.pitch, sizeof(underwaterVals.pitch));
        break;

      case GYRO_YAW_VAL_ROW:
        underwaterVals.yaw = readYaw();
        rs485.write((uint8_t*)&underwaterVals.yaw, sizeof(underwaterVals.yaw));
        break;

      case VOLTAGE_VAL_ROW:
        underwaterVals.voltage = base.busVoltage();
        rs485.write((uint8_t*)&underwaterVals.voltage, sizeof(underwaterVals.voltage));
        break;

      case CURRENT_VAL_ROW:
        underwaterVals.current = base.shuntCurrent();
        rs485.write((uint8_t*)&underwaterVals.current, sizeof(underwaterVals.current));
        break;

      case POWER_VAL_ROW:
        underwaterVals.power = base.busPower();
        rs485.write((uint8_t*)&underwaterVals.power, sizeof(underwaterVals.power));
        break;
    }
  }
}

void openDis(int num) {
  num = constrain(num, 0, 1);
  digitalWrite(dis_sw_pin, num & 1);
}

int16_t getDis(int sira) {

  bas:

  openDis(sira);

  int dis_val = -3;

  byte buffer_RTT[4];
  uint8_t CS;

  while (dis.available() > 0) dis.read();

  //delay(50);

  dis.write('+');
  delay(20);

  if (dis.available() > 0) {
    //delay(100);
    if (dis.read() == 0xff) {
      buffer_RTT[0] = 0xff;
      for (int i = 1; i < 4; i++) {
        buffer_RTT[i] = dis.read();
      }
      CS = buffer_RTT[0] + buffer_RTT[1] + buffer_RTT[2];
      if (buffer_RTT[3] == CS) {
        int Distance = (buffer_RTT[1] << 8) + buffer_RTT[2];
        dis_val = Distance;
      }
      //else return -1;
      //else goto bas;
      else dis_val = -1;
    }
    //else return -2;
    //else goto bas;
    else dis_val = -2;
  }
  //else return -3;
  //else goto bas;
  else dis_val = -3;

  return dis_val;
}

void readGyro() {
  mpu6050.update();
  gyro_vals.ax = mpu6050.getAccX();
  gyro_vals.ay = mpu6050.getAccY();
  gyro_vals.az = mpu6050.getAccZ();
  gyro_vals.gx = mpu6050.getGyroX();
  gyro_vals.gy = mpu6050.getGyroY();
  gyro_vals.gz = mpu6050.getGyroZ();
}

float readRoll() {
  readGyro();
  filter.updateIMU(gyro_vals.gx,
                   gyro_vals.gy,
                   gyro_vals.gz,
                   gyro_vals.ax,
                   gyro_vals.ay,
                   gyro_vals.az);
  return filter.getRoll();
}

float readPitch() {
  readGyro();
  filter.updateIMU(gyro_vals.gx,
                   gyro_vals.gy,
                   gyro_vals.gz,
                   gyro_vals.ax,
                   gyro_vals.ay,
                   gyro_vals.az);
  return filter.getPitch();
}

float readYaw() {
  readGyro();
  filter.updateIMU(gyro_vals.gx,
                   gyro_vals.gy,
                   gyro_vals.gz,
                   gyro_vals.ax,
                   gyro_vals.ay,
                   gyro_vals.az);
  return filter.getYaw();
}
