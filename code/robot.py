import json
import os
import threading
import time
from Raspi_MotorHAT.Raspi_PWM_Servo_Driver import PWM 
# from servos import Servos
from time import sleep

import atexit

# GENERAL TODO
# - use keyword parameters
# - use type hinting
# - proper error handling


PWM_ADDR = 0x40
PWM_FREQUENCY = 50
SERVO_MID_POINT_MS = 1.5
DEFLECT_90_IN_MS = 1

PERIOD_IN_MS = 1000 / PWM_FREQUENCY
PULSE_STEPS = 4096
OFF_STEPS_VALUE = 4096
STEPS_PER_MS = PULSE_STEPS / PERIOD_IN_MS

STEPS_PER_DEGREE = (DEFLECT_90_IN_MS * STEPS_PER_MS) / 90
SERVO_MID_POINT_STEPS = SERVO_MID_POINT_MS * STEPS_PER_MS

J1_CH = 0
J2_CH = 2
J3_CH = 4

HOME_J1 = 0
HOME_J2 = -48
HOME_J3 = 50

def convert_absolute_degrees_to_steps(position): 
    return int(SERVO_MID_POINT_STEPS + (position * STEPS_PER_DEGREE))

def convert_steps_to_absolute_degrees(steps):
    return int((steps - SERVO_MID_POINT_STEPS) / STEPS_PER_DEGREE)

def print_separator():
        print("---------------------------------------------")

def print_done():
        print("… DONE")

class Robot:

    def __init__(self, pwm_addr=PWM_ADDR):
        self._pwm = PWM(pwm_addr)
        # TODO make a class ASAP (OR NOT)
        # self.joints = {
        #     'j1': {'name': 'J1', 'channel': J1_CH, 'current_position': 0},
        #     'j2': {'name': 'J2', 'channel': J2_CH, 'current_position': 0},
        #     'j3': {'name': 'J3', 'channel': J3_CH, 'current_position': 0},
        # }
        # i guess bad practice but i dont give a fuck
        self.joint_names = (
            'J1',
            'J2',
            'J3'
        )
        self.joint_channels = (
            J1_CH,
            J2_CH,
            J3_CH
        )
        
        self.active_joint = {
            'name': None,
            'index': None,
            'channel': None,
            'position': None
        }
        self.home_joint_values = (
            HOME_J1,
            HOME_J2,
            HOME_J3
        )
        self._pwm.setPWMFreq(PWM_FREQUENCY)
        self.incremental_jog = 10
        self.is_incremental_jog = False
        self.gen_ovr = 0.1 # tweak this shit
        self.mip = False
        
        # self.servos = Servos(addr=pwm_addr)

        for i, _ in enumerate(self.joint_channels):
            self._pwm.setPWM(self.joint_channels[i], 0, convert_absolute_degrees_to_steps(self.home_joint_values[i]))

        self.current_joint_positions = [
            self.home_joint_values[0],
            self.home_joint_values[1],
            self.home_joint_values[2]
        ]
        
        atexit.register(self.stop_all)

    

    def set_active_joint(self, joint_index):
        print(f"SETTING JOINT {joint_index+1}")
        print_separator()
        self.active_joint['name'] = self.joint_names[joint_index]
        self.active_joint['index'] = joint_index
        self.active_joint['channel'] = self.joint_channels[joint_index]
        self.active_joint['position'] = self.current_joint_positions[joint_index]
        print_done()


    def stop_all_servos(self):
        print("STOPPING ALL SERVOS")
        print_separator()
        for joint in self.joint_channels:
            self._pwm.setPWM(joint, 0, OFF_STEPS_VALUE)
        print_done()
                

    def stop_all(self): 
        print("STOPPING ALL")
        print_separator()
        self.stop_all_servos() 
        # self.leds.clear() 
        # self.leds.show()
        print_done()


    def go_home(self):
        print("GOING HOME (i wish)")
        print_separator()
        self.joint_movement(self.home_joint_values)
        print_done()
        self.show_current_positions()

    def go_ready(self):
        pass
        # self.show_current_positions()

    def show_current_positions(self):
        print("CURRENT JOINT VALUES")
        print_separator()
        for i, joint_value in enumerate(self.current_joint_positions):
            print(f"{self.joint_names[i]}\t{joint_value}°")
        print_done()

    # meh
    def set_gen_ovr(self, value):
        if 0 < value <= 100:
            self.gen_ovr = value
        else:
            raise ValueError("Invalid value. Must be between 0 and 100.")
        print(f"GEN_OVR IS {self.gen_ovr}%")
        print_done()

    # MEH
    def show_gen_ovr(self):
        print(f"GEN_OVR IS {self.gen_ovr}%")

    def go_zero(self):
        print("GOING ZERO")
        print_separator()
        self.joint_movement([0, 0, 0])
        print_done()
        self.show_current_positions()

    def go_cal_sys(self):
        print("GOING CAL SYS")
        print_separator()
        for channel in self.joint_channels:
            self._pwm.setPWM(channel, 0, convert_absolute_degrees_to_steps(0))
        self.current_joint_positions = [0, 0, 0]
        print_done()

    # def move_joint_absolute(self, joint, position):
    #     self._pwm.setPWM(self.get_joint_channel(joint), 0, position)
    #     self.current_joint_positions[joint] = position

    # todo can i integrate this with joint_movement?
    def move_joint_relative(self, joint, change):
        print("MOVING JOINT RELATIVE")
        print_separator()
        # print(joint)
        current_position = self.current_joint_positions[joint]

        end_position = self.current_joint_positions[joint] + change
        if self.stroke_end(end_position):
            print("STROKE END")
            return

        start_step = convert_absolute_degrees_to_steps(current_position)
        end_step = convert_absolute_degrees_to_steps(end_position)
        step = 1 if end_step > start_step else -1

        for position in range(start_step, end_step, step):
            self._pwm.setPWM(self.joint_channels[joint], 0, position)
            sleep(self.gen_ovr)
        self._pwm.setPWM(self.joint_channels[joint], 0, end_step)

        self.current_joint_positions[joint] = end_position
        print_done()
        self.show_current_positions()

    def joint_movement(self, target_positions):
        # todo fix this sh
        print("JOINT MOVEMENT")
        print_separator()

        DEGREES_PER_STEP = 2
        diffs = []
        for i in range(len(self.joint_channels)):
            diffs.append(abs(target_positions[i] - self.current_joint_positions[i]))

        steps_needed = max(diffs) / DEGREES_PER_STEP

        deg_steps = []

        for i in range(len(self.joint_channels)):
            deg_steps.append((diffs[i] / steps_needed))

        directions = []

        for i in range(len(self.joint_channels)):
            directions.append(1 if target_positions[i] > self.current_joint_positions[i] else -1)

        for _ in range(int(steps_needed)):
            for index in range(len(self.joint_channels)):
                self.current_joint_positions[index] += deg_steps[index] * directions[index]
                self._pwm.setPWM(self.joint_channels[index], 0, convert_absolute_degrees_to_steps(self.current_joint_positions[index]))
            sleep(self.gen_ovr)

        for index in range(len(self.joint_channels)):
            self._pwm.setPWM(self.joint_channels[index], 0, convert_absolute_degrees_to_steps(target_positions[index]))
        
        print_done()
        self.show_current_positions()

    # def toggle_incremental_jog(self):
    #     self.is_incremental_jog = not self.is_incremental_jog
    #     print(f"INCREMENTAL JOG IS {self.is_incremental_jog}")

    def set_incremental_jog(self, value):
        if 0 < value <= 90:
            self.incremental_jog = value
        else:
            raise ValueError("Invalid value. Must be between 0 and 90.")
        print(f"INCR_JOG IS {self.incremental_jog}")

    def show_status(self):
        print("STATUS")
        print_separator()
        print(f"ACTIVE JOINT IS {self.active_joint['name']}")
        print(f"INCR_JOG IS {self.incremental_jog}")
        # print(f"GEN_OVR IS 100%") # USELESS
        # print(f"GEN_OVR IS {self.gen_ovr}%")
        self.show_current_positions()

    def return_status(self):
        return json.dumps({
            'incremental_jog': self.incremental_jog,
            'j1': self.current_joint_positions[0],
            'j2': self.current_joint_positions[1],
            'j3': self.current_joint_positions[2]
        })
        # return self.current_joint_positions


    def move_joint_incremental(self, joint, direction):
        if self.mip:
            print("Movement already in progress.")
            return
        def movement_task():
            self.mip = True
            print("MOVING JOINT INCREMENTAL")
            print_separator()
            change = direction * self.incremental_jog
            self.move_joint_relative(joint, change)
            print_done()
            self.show_current_positions()
            self.mip = False
        threading.Thread(target=movement_task, daemon=True).start()


    def stroke_end(self, value):
        return value < -89 or value > 89
    


    # def convert_speed(self, speed):
    #     mode = Raspi_MotorHAT.RELEASE
    #     if speed > 0:
    #         mode = Raspi_MotorHAT.FORWARD
    #     elif speed < 0:
    #         mode = Raspi_MotorHAT.BACKWARD
    #     output_speed = (abs(speed) * MAX_SPEED) // 100
    #     return mode, int(output_speed)

    # def set_left(self, speed):
    #     mode, output_speed = self.convert_speed(speed)
    #     self.left_motor.setSpeed(output_speed)
    #     self.left_motor.run(mode)

    # def set_right(self, speed):
    #     mode, output_speed = self.convert_speed(speed)
    #     self.right_motor.setSpeed(output_speed)
    #     self.right_motor.run(mode)
        
    # def stop_motors(self):
    #     self.left_motor.run(Raspi_MotorHAT.RELEASE)
    #     self.right_motor.run(Raspi_MotorHAT.RELEASE)

    # def sensors_trig(self, frequency):
    #     while(True):
    #         ld, rd = round(self.sensor_l.distance * 1000, 1), round(self.sensor_r.distance * 1000, 1)
    #         # meh
    #         if ld == 1000.0:
    #             ld = "INF"
    #         else:
    #             ld = str(ld) + " mm"
    #         if rd == 1000.0:
    #             rd = "INF"
    #         else:
    #             rd = str(rd) + " mm"
    #         print(f'LEFT {ld}\tRIGHT {rd}')
    #         time.sleep(frequency)

    
