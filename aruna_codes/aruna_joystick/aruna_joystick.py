#from serial import Serial
from time import sleep
from ps4_control import PS4Control
import struct
from threading import Thread, Timer
from rov_control import rovVehicle
import signal
import atexit

def constrain(val, min_, max_):
    if val > max_:
        return max_
    elif val < min_:
        return min_
    else:
        return val

port = "COM12"
baud = 9600

aruna = rovVehicle(port, baud)
sleep(3)
print("System started.")

aruna.stopAllMotors()

ps4 = PS4Control(0)

speed = 250

def getSensors():

    if True:
    #while True:

        dis_front = aruna.getFrontDis()
        dis_lower = aruna.getLowerDis()

        roll = aruna.getRoll()
        pitch = aruna.getPitch()
        yaw = aruna.getYaw()

        voltage = aruna.getVoltage()
        current = aruna.getCurrent()
        power = aruna.getPower()

        print("Front Dis:", dis_front)
        print("Lower Dis:", dis_lower)

        print("Roll:", roll)
        print("Pitch:", pitch)
        print("Yaw:", yaw)

        print("Votlage:", voltage)
        print("Current:", current)
        print("Power:", power)

        print("==========================================")

        #sleep(0.5)

        Timer(0.5, getSensors).start()

def vehicleControl():

    global speed

    while True:

        try:

            #getSensors()

            vals = ps4.check(wait_for_change = True)

            #getSensors()

            if vals["R3-Y"] == -1:
                aruna.goForward(speed, speed)

            elif vals["R3-Y"] == 1:
                aruna.goBackward(speed, speed)

            elif vals["R3-X"] == 1 and vals["R3-Y"] == 0:
                aruna.turnRight(speed)

            elif vals["R3-X"] == -1 and vals["R3-Y"] == 0:
                aruna.turnLeft(speed)

            elif vals["R1"] and not vals["L1"]:
                aruna.goRight(speed, speed)

            elif vals["L1"] and not vals["R1"]:
                aruna.goLeft(speed, speed)

            else:
                aruna.stopLowerMotors()

            if vals["L3-Y"] == -1:
                aruna.goUp(speed)

            elif vals["L3-Y"] == 1:
                aruna.goDown(speed)

            elif vals["L3-X"] == 1 and vals["L3-Y"] == 0:
                aruna.liftFront(speed)

            elif vals["L3-X"] == -1 and vals["L3-Y"] == 0:
                aruna.liftBack(speed)

            elif vals["R2"] and not vals["L2"]:
                aruna.liftRight(speed)

            elif vals["L2"] and not vals["R2"]:
                aruna.liftLeft(speed)

            else:
                aruna.stopUpperMotors()

            if vals["Up Arrow"] and not vals["Down Arrow"]:
                speed += 50
                speed = constrain(speed, 0, 500)

            elif vals["Down Arrow"] and not vals["Up Arrow"]:
                speed -= 50
                speed = constrain(speed, 0, 500)

            if vals["Square"]:
                aruna.setRelay0(1)

            else:
                aruna.setRelay0(0)

            if vals["Triangle"]:
                aruna.setRelay1(1)

            else:
                aruna.setRelay1(0)

            if vals["Circle"]:
                aruna.setRelay2(1)

            else:
                aruna.setRelay2(0)

        except:
            aruna.stopAllMotors()
            break

aruna.setFilterReset(1)
aruna.setFilterReset(0)

def closingMoment(signum = None, frame = None):
    aruna.stopAllMotors()

signal.signal(signal.SIGINT, closingMoment)
signal.signal(signal.SIGTERM, closingMoment)

atexit.register(closingMoment)

#sensor_read = Thread(target = getSensors)
#sensor_read.start()

#getSensors()

vehicleControl()
