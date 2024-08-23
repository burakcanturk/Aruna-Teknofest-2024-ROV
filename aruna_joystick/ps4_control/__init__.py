import pygame
import os
import json
from time import sleep

pygame.init()
pygame.joystick.init()

class PS4Control:

    def __init__(self, port_number = 0):

        if __name__ != "__main__":
            with open(os.path.join("ps4_control\\ps4_keys.json"), 'r') as file:
                self.ps4_keys = json.load(file)
                file.close()

        else:
            with open(os.path.join("ps4_keys.json"), 'r') as file:
                self.ps4_keys = json.load(file)
                file.close()

        self.analog_keys = self.ps4_keys["analog_keys"]
        self.analog_keys_reversed = {v: k for k, v in self.analog_keys.items()}

        self.L2_default = self.ps4_keys["analog_values"]["L2"]["default"]
        self.R2_default = self.ps4_keys["analog_values"]["R2"]["default"]
        self.L3_X_default = self.ps4_keys["analog_values"]["L3"]["X"]["default"]
        self.L3_Y_default = self.ps4_keys["analog_values"]["L3"]["Y"]["default"]
        self.R3_X_default = self.ps4_keys["analog_values"]["R3"]["X"]["default"]
        self.R3_Y_default = self.ps4_keys["analog_values"]["R3"]["Y"]["default"]

        self.analog_values = {
            "L2":   self.L2_default,
            "R2":   self.R2_default,
            "L3-X": self.L3_X_default,
            "L3-Y": self.L3_Y_default,
            "R3-X": self.R3_X_default,
            "R3-Y": self.R3_Y_default
        }

        self.analog_values_before = self.analog_values.copy()

        """self.L2_pressed = False
        self.R2_pressed = False
        self.L3_X_location = 0
        self.L3_Y_location = 0
        self.R3_X_location = 0
        self.R3_Y_location = 0"""

        self.button_keys = self.ps4_keys["buttons"]
        self.button_keys_reversed = {v: k for k, v in self.button_keys.items()}

        self.values = {
            "X":	    False,
	    "Circle":	    False,
	    "Square":	    False,
	    "Triangle":	    False,
	    "Share":	    False,
	    "PS":	    False,
	    "Options":	    False,
	    "L3":	    False,
	    "R3":	    False,
	    "L1":	    False,
	    "R1":	    False,
	    "Up Arrow":	    False,
	    "Down Arrow":   False,
	    "Left Arrow":   False,
	    "Right Arrow":  False,
	    "Touchpad":	    False,
            "L2":	    False,
	    "R2":	    False,
            "L3-X":	    0,
	    "L3-Y":	    0,
	    "R3-X":	    0,
	    "R3-Y":	    0,
        }

        self.buttons = list(self.values.keys())

        self.values_before = self.values.copy()

        self.joystick = pygame.joystick.Joystick(port_number)
        self.joystick.init()

    def check(self, wait_for_change = False):

        while True:

            for event in pygame.event.get():

                if event.type == pygame.JOYBUTTONDOWN:
                    self.values[self.button_keys_reversed[event.button]] = True

                if event.type == pygame.JOYBUTTONUP:
                    self.values[self.button_keys_reversed[event.button]] = False
                
                if event.type == pygame.JOYAXISMOTION:
                    self.analog_values[self.analog_keys_reversed[event.axis]] = round(event.value, 2)

            if self.analog_values["L2"] != self.analog_values_before["L2"]:
                min_ = self.ps4_keys["analog_values"]["L2"]["min"]
                max_ = self.ps4_keys["analog_values"]["L2"]["max"]
                pressed = min_ <= self.analog_values["L2"] <= max_
                self.values["L2"] = pressed

            if self.analog_values["R2"] != self.analog_values_before["R2"]:
                min_ = self.ps4_keys["analog_values"]["R2"]["min"]
                max_ = self.ps4_keys["analog_values"]["R2"]["max"]
                pressed = min_ <= self.analog_values["R2"] <= max_
                self.values["R2"] = pressed

            if self.analog_values["L3-X"] != self.analog_values_before["L3-X"]:
                left_ = self.ps4_keys["analog_values"]["L3"]["X"]["left"]
                right_ = self.ps4_keys["analog_values"]["L3"]["X"]["right"]
                is_left = self.analog_values["L3-X"] <= left_
                is_right = self.analog_values["L3-X"] >= right_
                if is_left:
                    self.values["L3-X"] = -1
                elif is_right:
                    self.values["L3-X"] = 1
                else:
                    self.values["L3-X"] = 0

            if self.analog_values["L3-Y"] != self.analog_values_before["L3-Y"]:
                up_ = self.ps4_keys["analog_values"]["L3"]["Y"]["up"]
                down_ = self.ps4_keys["analog_values"]["L3"]["Y"]["down"]
                is_up = self.analog_values["L3-Y"] <= up_
                is_down = self.analog_values["L3-Y"] >= down_
                if is_up:
                    self.values["L3-Y"] = -1
                elif is_down:
                    self.values["L3-Y"] = 1
                else:
                    self.values["L3-Y"] = 0

            if self.analog_values["R3-X"] != self.analog_values_before["R3-X"]:
                left_ = self.ps4_keys["analog_values"]["R3"]["X"]["left"]
                right_ = self.ps4_keys["analog_values"]["R3"]["X"]["right"]
                is_left = self.analog_values["R3-X"] <= left_
                is_right = self.analog_values["R3-X"] >= right_
                if is_left:
                    self.values["R3-X"] = -1
                elif is_right:
                    self.values["R3-X"] = 1
                else:
                    self.values["R3-X"] = 0

            if self.analog_values["R3-Y"] != self.analog_values_before["R3-Y"]:
                up_ = self.ps4_keys["analog_values"]["R3"]["Y"]["up"]
                down_ = self.ps4_keys["analog_values"]["R3"]["Y"]["down"]
                is_up = self.analog_values["R3-Y"] <= up_
                is_down = self.analog_values["R3-Y"] >= down_
                if is_up:
                    self.values["R3-Y"] = -1
                elif is_down:
                    self.values["R3-Y"] = 1
                else:
                    self.values["R3-Y"] = 0

            self.analog_values_before = self.analog_values.copy()

            if not wait_for_change or self.values != self.values_before:
                break

            self.values_before = self.values.copy()

        self.values_before = self.values.copy()

        return self.values

if __name__ == "__main__":
    ps4 = PS4Control(0)
    while True:
        check = ps4.check(wait_for_change = True)
        for k, v in check.items():
            print(f"{k}: {v}")
        print()
        sleep(0.5)
