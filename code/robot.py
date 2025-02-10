import os
import time
from Raspi_MotorHAT.Raspi_PWM_Servo_Driver import PWM 
# from servos import Servos
from time import sleep

import atexit




PWM_ADDR = 0x40
PWM_FREQUENCY = 50
SERVO_MID_POINT_MS = 1.5
DEFLECT_90_IN_MS = 1

PERIOD_IN_MS = 1000 / PWM_FREQUENCY
PULSE_STEPS = 4096
STEPS_PER_MS = PULSE_STEPS / PERIOD_IN_MS

STEPS_PER_DEGREE = (DEFLECT_90_IN_MS * STEPS_PER_MS) / 90
SERVO_MID_POINT_STEPS = SERVO_MID_POINT_MS * STEPS_PER_MS

J1_CH = 0
J2_CH = 2
J3_CH = 4

HOME_J1 = 0
HOME_J2 = -50
HOME_J3 = 50

def convert_absolute_degrees_to_steps(position): 
    return int(SERVO_MID_POINT_STEPS + (position * STEPS_PER_DEGREE))

# JOINT
# IS
# A
# STRING!!

class Robot:

    def __init__(self, pwm_addr=PWM_ADDR):
        self._pwm = PWM(pwm_addr)
        # TODO make a class ASAP
        self.joints = {
            'j1': {'name': 'J1', 'channel': J1_CH, 'current_position': 0},
            'j2': {'name': 'J2', 'channel': J2_CH, 'current_position': 0},
            'j3': {'name': 'J3', 'channel': J3_CH, 'current_position': 0},
        }
        # self.current_joint_positions = {
        #     'j1': 0,
        #     'j2': 0,
        #     'j3': 0
        # }
        self._pwm.setPWMFreq(PWM_FREQUENCY)
        self.incremental_jog = None
        self.is_incremental_jog = False
        self.gen_ovr = 0.01 # tweak this shit
        
        # self.servos = Servos(addr=pwm_addr)
        self.active_joint = None
        
        atexit.register(self.stop_all)

    # sort this shit out
    def joint_selection(self, choice):
        if choice == "1":
            joint = 'j1'
        elif choice == "2":
            joint = 'j2'
        elif choice == "3":
            joint = 'j3'
        return joint       

    def set_active_joint(self, joint):
        self.active_joint = joint

    def get_joint_channel(self, joint):
        return self.joints[joint]['channel']

    def stop_all_servos(self):
        for joint in self.joints.values():
            self._pwm.setPWM(joint['channel'], 0, 4096)        

    def stop_all(self): 
        self.stop_all_servos() 
        # self.leds.clear() 
        # self.leds.show()

    def go_home(self):
        # STUPID
        self._pwm.setPWM(self.joints['j1']['channel'], 0, convert_absolute_degrees_to_steps(HOME_J1))
        self.joints['j1']['current_position'] = HOME_J1
        self._pwm.setPWM(self.joints['j2']['channel'], 0, convert_absolute_degrees_to_steps(HOME_J2))
        self.joints['j2']['current_position'] = HOME_J2
        self._pwm.setPWM(self.joints['j3']['channel'], 0, convert_absolute_degrees_to_steps(HOME_J3))
        self.joints['j3']['current_position'] = HOME_J3

    def go_ready(self):
        pass

    def show_current_positions(self):
        for joint in self.joints.values():
            print(f"{joint['name']}\t{joint['current_position']}")

    def set_gen_ovr(self, value):
        if 0 < value <= 100:
            self.gen_ovr = value
        else:
            raise ValueError("Invalid value. Must be between 0 and 100.")
        print(f"GEN_OVR IS {self.gen_ovr}%")
        
    def show_gen_ovr(self):
        print(f"GEN_OVR IS {self.gen_ovr}%")

    def go_zero(self):
        for joint in self.joints.values():
            self._pwm.setPWM(joint['channel'], 0, convert_absolute_degrees_to_steps(0))
            joint['current_position'] = 0

    # def move_joint_absolute(self, joint, position):
    #     self._pwm.setPWM(self.get_joint_channel(joint), 0, position)
    #     self.current_joint_positions[joint] = position

    def move_joint_relative(self, joint, end_position):
        if self.stroke_end(end_position):
            print("STROKE END")
            return
        current_position = self.joints[joint]['current_position']

        
        start_step = convert_absolute_degrees_to_steps(current_position)
        end_step = convert_absolute_degrees_to_steps(end_position)
        step = 1 if end_step > start_step else -1

        for position in range(start_step, end_step, step):
            self._pwm.setPWM(self.get_joint_channel(joint), 0, position)
            sleep(self.gen_ovr)
        self._pwm.setPWM(self.get_joint_channel(joint), 0, end_step)

        self.joints[joint]['current_position'] = end_position

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
        print(f"ACTIVE JOINT IS {self.active_joint}")
        print(f"INCR_JOG IS {self.incremental_jog}")
        print(f"GEN_OVR IS 100%") # USELESS
        # print(f"GEN_OVR IS {self.gen_ovr}%")
        self.show_current_positions()

    def move_joint_incremental(self, joint, direction):
        current_position = self.joints[joint]['current_position']
        new_position = current_position + direction * self.incremental_jog
        self.move_joint_relative(joint, new_position)

    def stroke_end(self, value):
        return value < -89 or value > 89
    
    def set_active_joint(self, joint):
        self.active_joint = joint

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

    
