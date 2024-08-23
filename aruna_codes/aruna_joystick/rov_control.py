from serial import Serial
import struct
from time import sleep

URF_VAL_ROW = 0
ULF_VAL_ROW = 1
URB_VAL_ROW = 2
ULB_VAL_ROW = 3
LRF_VAL_ROW = 4
LLF_VAL_ROW = 5
LRB_VAL_ROW = 6
LLB_VAL_ROW = 7
RELAY0_VAL_ROW = 8
RELAY1_VAL_ROW = 9
RELAY2_VAL_ROW = 10
FILTER_RESET_ROW = 11
GYRO_CALIB_ROW = 12

FRONT_DIS_VAL_ROW = 128
LOWER_DIS_VAL_ROW = 129
GYRO_ROLL_VAL_ROW = 130
GYRO_PITCH_VAL_ROW = 131
GYRO_YAW_VAL_ROW = 132
VOLTAGE_VAL_ROW = 133
CURRENT_VAL_ROW = 134
POWER_VAL_ROW = 135

ESC_MIN = 1000
ESC_STOP = 1500
ESC_MAX = 2000

landVals = {
    "upper_right_front_val": ESC_STOP,
    "upper_left_front_val": ESC_STOP,
    "upper_right_back_val": ESC_STOP,
    "upper_left_back_val": ESC_STOP,
    "lower_right_front_val": ESC_STOP,
    "lower_left_front_val": ESC_STOP,
    "lower_right_back_val": ESC_STOP,
    "lower_left_back_val": ESC_STOP,
    "relay0_val": 0,
    "relay1_val": 0,
    "relay2_val": 0,
    "filter_reset": 0,
    "gyro_calib": 0
}

underwaterVals = {
    "dis_front_val": 0,
    "dis_lower_val": 0,
    "roll": 0.0,
    "pitch": 0.0,
    "yaw": 0.0,
    "voltage": 0.0,
    "current": 0.0,
    "power": 0.0,
}

def constrain(val, min_, max_):
    if val > max_:
        return max_
    elif val < min_:
        return min_
    else:
        return val
    

class rovVehicle(Serial):

    def __init__(self, port, baud):
        self.__init__(port, baud)

    def readSignalReceived(self):
        #self.read(1)
        pass

    def setUpperRightFrontMotor(self, speed):
        landVals["upper_right_front_val"] = constrain(speed, ESC_MIN, ESC_MAX)
        self.write(URF_VAL_ROW.to_bytes(1, "little"))
        self.write(landVals["upper_right_front_val"].to_bytes(2, "little"))
        self.readSignalReceived()

    def setUpperLeftFrontMotor(self, speed):
        landVals["upper_left_front_val"] = constrain(speed, ESC_MIN, ESC_MAX)
        self.write(ULF_VAL_ROW.to_bytes(1, "little"))
        self.write(landVals["upper_left_front_val"].to_bytes(2, "little"))
        self.readSignalReceived()

    def setUpperRightBackMotor(self, speed):
        landVals["upper_right_back_val"] = constrain(speed, ESC_MIN, ESC_MAX)
        self.write(URB_VAL_ROW.to_bytes(1, "little"))
        self.write(landVals["upper_right_back_val"].to_bytes(2, "little"))
        self.readSignalReceived()

    def setUpperLeftBackMotor(self, speed):
        landVals["upper_left_back_val"] = constrain(speed, ESC_MIN, ESC_MAX)
        self.write(ULB_VAL_ROW.to_bytes(1, "little"))
        self.write(landVals["upper_left_back_val"].to_bytes(2, "little"))
        self.readSignalReceived()

    def setLowerRightFrontMotor(self, speed):
        landVals["lower_right_front_val"] = constrain(speed, ESC_MIN, ESC_MAX)
        self.write(LRF_VAL_ROW.to_bytes(1, "little"))
        self.write(landVals["lower_right_front_val"].to_bytes(2, "little"))
        self.readSignalReceived()

    def setLowerLeftFrontMotor(self, speed):
        landVals["lower_left_front_val"] = constrain(speed, ESC_MIN, ESC_MAX)
        self.write(LLF_VAL_ROW.to_bytes(1, "little"))
        self.write(landVals["lower_left_front_val"].to_bytes(2, "little"))
        self.readSignalReceived()

    def setLowerRightBackMotor(self, speed):
        landVals["lower_right_back_val"] = constrain(speed, ESC_MIN, ESC_MAX)
        self.write(LRB_VAL_ROW.to_bytes(1, "little"))
        self.write((3000 - landVals["lower_right_back_val"]).to_bytes(2, "little"))
        self.readSignalReceived()

    def setLowerLeftBackMotor(self, speed):
        landVals["lower_left_back_val"] = constrain(speed, ESC_MIN, ESC_MAX)
        self.write(LLB_VAL_ROW.to_bytes(1, "little"))
        self.write((3000 - landVals["lower_left_back_val"]).to_bytes(2, "little"))
        self.readSignalReceived()

    def setRelay0(self, val):
        landVals["relay0_val"] = constrain(val, 0, 1)
        self.write(RELAY0_VAL_ROW.to_bytes(1, "little"))
        self.write(landVals["relay0_val"].to_bytes(1, "little"))
        self.readSignalReceived()

    def setRelay1(self, val):
        landVals["relay1_val"] = constrain(val, 0, 1)
        self.write(RELAY1_VAL_ROW.to_bytes(1, "little"))
        self.write(landVals["relay1_val"].to_bytes(1, "little"))
        self.readSignalReceived()

    def setRelay2(self, val):
        landVals["relay2_val"] = constrain(val, 0, 1)
        self.write(RELAY2_VAL_ROW.to_bytes(1, "little"))
        self.write(landVals["relay2_val"].to_bytes(1, "little"))
        self.readSignalReceived()

    def setFilterReset(self, val):
        landVals["filter_reset"] = constrain(val, 0, 1)
        self.write(FILTER_RESET_ROW.to_bytes(1, "little"))
        self.write(landVals["filter_reset"].to_bytes(1, "little"))
        self.readSignalReceived()

    def setGyroCalib(self, val):
        landVals["gyro_calib"] = constrain(val, 0, 1)
        self.write(GYRO_CALIB_ROW.to_bytes(1, "little"))
        self.write(landVals["gyro_calib"].to_bytes(1, "little"))
        self.readSignalReceived()

    def stopLowerMotors(self):
        self.setLowerRightFrontMotor(ESC_STOP)
        self.setLowerLeftFrontMotor(ESC_STOP)
        self.setLowerRightBackMotor(ESC_STOP)
        self.setLowerLeftBackMotor(ESC_STOP)

    def stopUpperMotors(self):
        self.setUpperRightFrontMotor(ESC_STOP)
        self.setUpperLeftFrontMotor(ESC_STOP)
        self.setUpperRightBackMotor(ESC_STOP)
        self.setUpperLeftBackMotor(ESC_STOP)

    def butunMotorlarDurdur(self):
        self.stopLowerMotors()
        self.stopUpperMotors()

    #-----------------------------------------------------------------------

    def goForward(self, left_speed, right_speed):
        self.setLowerRightFrontMotor(ESC_STOP + (constrain(right_speed, 0, 500)))
        self.setLowerLeftFrontMotor(ESC_STOP + (constrain(right_speed, 0, 500)))
        self.setLowerRightBackMotor(ESC_STOP + (constrain(right_speed, 0, 500)))
        self.setLowerLeftBackMotor(ESC_STOP + (constrain(right_speed, 0, 500)))

    def goBackward(self, left_speed, right_speed):
        self.setLowerRightFrontMotor(ESC_STOP - constrain(right_speed, 0, 500))
        self.setLowerLeftFrontMotor(ESC_STOP - constrain(left_speed, 0, 500))
        self.setLowerRightBackMotor(ESC_STOP - constrain(right_speed, 0, 500))
        self.setLowerLeftBackMotor(ESC_STOP - constrain(left_speed, 0, 500))

    def turnRight(self, speed):
        self.setLowerRightFrontMotor(ESC_STOP - constrain(speed, 0, 500))
        self.setLowerLeftFrontMotor(ESC_STOP + constrain(speed, 0, 500))
        self.setLowerRightBackMotor(ESC_STOP - constrain(speed, 0, 500))
        self.setLowerLeftBackMotor(ESC_STOP + constrain(speed, 0, 500))

    def turnLeft(self, speed):
        self.setLowerRightFrontMotor(ESC_STOP + constrain(speed, 0, 500))
        self.setLowerLeftFrontMotor(ESC_STOP - constrain(speed, 0, 500))
        self.setLowerRightBackMotor(ESC_STOP + constrain(speed, 0, 500))
        self.setLowerLeftBackMotor(ESC_STOP - constrain(speed, 0, 500))

    def goRight(self, left_speed, right_speed):
        self.setLowerRightFrontMotor(ESC_STOP - constrain(right_speed, 0, 500))
        self.setLowerLeftFrontMotor(ESC_STOP + constrain(left_speed, 0, 500))
        self.setLowerRightBackMotor(ESC_STOP + constrain(right_speed, 0, 500))
        self.setLowerLeftBackMotor(ESC_STOP - constrain(left_speed, 0, 500))

    def goLeft(self, left_speed, right_speed):
        self.setLowerRightFrontMotor(ESC_STOP + constrain(right_speed, 0, 500))
        self.setLowerLeftFrontMotor(ESC_STOP - constrain(left_speed, 0, 500))
        self.setLowerRightBackMotor(ESC_STOP - constrain(right_speed, 0, 500))
        self.setLowerLeftBackMotor(ESC_STOP + constrain(left_speed, 0, 500))

    def goUp(self, speed):
        self.setUpperRightFrontMotor(ESC_STOP + constrain(speed, 0, 500))
        self.setUpperLeftFrontMotor(ESC_STOP + constrain(speed, 0, 500))
        self.setUpperRightBackMotor(ESC_STOP + constrain(speed, 0, 500))
        self.setUpperLeftBackMotor(ESC_STOP + constrain(speed, 0, 500))

    def goDown(self, speed):
        self.setUpperRightFrontMotor(ESC_STOP - constrain(speed, 0, 500))
        self.setUpperLeftFrontMotor(ESC_STOP - constrain(speed, 0, 500))
        self.setUpperRightBackMotor(ESC_STOP - constrain(speed, 0, 500))
        self.setUpperLeftBackMotor(ESC_STOP - constrain(speed, 0, 500))

    def liftFront(self, speed):
        self.setUpperRightFrontMotor(ESC_STOP + constrain(speed, 0, 500))
        self.setUpperLeftFrontMotor(ESC_STOP + constrain(speed, 0, 500))
        self.setUpperRightBackMotor(ESC_STOP - constrain(speed, 0, 500))
        self.setUpperLeftBackMotor(ESC_STOP - constrain(speed, 0, 500))

    def liftBack(self, speed):
        self.setUpperRightFrontMotor(ESC_STOP - constrain(speed, 0, 500))
        self.setUpperLeftFrontMotor(ESC_STOP - constrain(speed, 0, 500))
        self.setUpperRightBackMotor(ESC_STOP + constrain(speed, 0, 500))
        self.setUpperLeftBackMotor(ESC_STOP + constrain(speed, 0, 500))

    def liftRight(self, speed):
        self.setUpperRightFrontMotor(ESC_STOP + constrain(speed, 0, 500))
        self.setUpperLeftFrontMotor(ESC_STOP - constrain(speed, 0, 500))
        self.setUpperRightBackMotor(ESC_STOP + constrain(speed, 0, 500))
        self.setUpperLeftBackMotor(ESC_STOP - constrain(speed, 0, 500))

    def liftLeft(self, speed):
        self.setUpperRightFrontMotor(ESC_STOP - constrain(speed, 0, 500))
        self.setUpperLeftFrontMotor(ESC_STOP + constrain(speed, 0, 500))
        self.setUpperRightBackMotor(ESC_STOP - constrain(speed, 0, 500))
        self.setUpperLeftBackMotor(ESC_STOP + constrain(speed, 0, 500))

    #---------------------------------------------------

    def getFrontDis(self):
        self.write(FRONT_DIS_VAL_ROW.to_bytes(1, "little"))
        landVals["dis_front_val"] = int.from_bytes(self.read(2), "little", signed = True)
        return landVals["dis_front_val"]

    def getLowerDis(self):
        self.write(LOWER_DIS_VAL_ROW.to_bytes(1, "little"))
        landVals["on_asagi_val"] = int.from_bytes(self.read(2), "little", signed = True)
        return landVals["on_asagi_val"]

    def getRoll(self):
        self.write(GYRO_ROLL_VAL_ROW.to_bytes(1, "little"))
        landVals["roll"] = round(struct.unpack("f", self.read(4))[0], 2)
        return landVals["roll"]

    def getPitch(self):
        self.write(GYRO_PITCH_VAL_ROW.to_bytes(1, "little"))
        landVals["pitch"] = round(struct.unpack("f", self.read(4))[0], 2)
        return landVals["pitch"]

    def getYaw(self):
        self.write(GYRO_YAW_VAL_ROW.to_bytes(1, "little"))
        landVals["yaw"] = round(struct.unpack("f", self.read(4))[0], 2)
        return landVals["yaw"]

    def getVoltage(self):
        self.write(VOLTAGE_VAL_ROW.to_bytes(1, "little"))
        landVals["voltage"] = round(struct.unpack("f", self.read(4))[0], 2)
        return landVals["voltage"]

    def getCurrent(self):
        self.write(CURRENT_VAL_ROW.to_bytes(1, "little"))
        landVals["current"] = round(struct.unpack("f", self.read(4))[0], 2)
        return landVals["current"]

    def getPower(self):
        self.write(POWER_VAL_ROW.to_bytes(1, "little"))
        landVals["power"] = round(struct.unpack("f", self.read(4))[0], 2)
        return landVals["power"]
