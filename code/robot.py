import os
import time
from Raspi_MotorHAT.Raspi_PWM_Servo_Driver import PWM 
from servos import Servos

import atexit




PWM_ADDR = 0x40

J1_CH = 0
J2_CH = 2
J3_CH = 4



class Robot:

    def __init__(self, pwm_addr=PWM_ADDR):
        self._pwm = PWM(pwm_addr)
        self.joints = {
            'j1': J1_CH,
            'j2': J2_CH,
            'j3': J3_CH
        }
        self.servos = Servos(addr=pwm_addr)
        atexit.register(self.stop_all)

    def stop_all_servos(self):
        for joint, channel in self.joints:
            self._pwm.setPWM(channel, 0, 0)        

    def stop_all(self): 
        self.stop_all_servos() 
        # self.leds.clear() 
        # self.leds.show()

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

    
