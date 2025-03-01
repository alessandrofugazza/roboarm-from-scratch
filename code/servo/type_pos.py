from Raspi_MotorHAT.Raspi_PWM_Servo_Driver import PWM 
import atexit
from time import sleep

pwm = PWM(0x40)

pwm_frequency = 50
pwm.setPWMFreq(pwm_frequency)

# SERVO_TYPE = 1
SERVO_TYPE = 0.69
servo_mid_point_ms = 1.5
# servo_mid_point_ms = 1

deflect_90_in_ms = SERVO_TYPE

period_in_ms = 1000 / pwm_frequency
pulse_steps = 4096
steps_per_ms = pulse_steps / period_in_ms

steps_per_degree = (deflect_90_in_ms * steps_per_ms) / 90
servo_mid_point_steps = servo_mid_point_ms * steps_per_ms

def convert_degrees_to_steps(position): 
    return int(servo_mid_point_steps + (position * steps_per_degree))

# servo_channels = [13, 15]
servo_channel = 15

def turn_off_servos():
    pwm.setPWM(servo_channel, 0, 4096)

atexit.register(turn_off_servos)


servo_channel, 0, convert_degrees_to_steps(0)

current_position = 0

while True: 

    target_position = int(input("Type your position in degrees (90 to -90, 0 is middle): "))

    
    pwm_value = convert_degrees_to_steps(target_position)
    pwm.setPWM(servo_channel, 0, pwm_value)
    current_positions = target_position

