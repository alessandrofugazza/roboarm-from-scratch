from Raspi_MotorHAT.Raspi_PWM_Servo_Driver import PWM 
import atexit

pwm = PWM(0x40)

pwm_frequency = 50 
pwm.setPWMFreq(pwm_frequency)

servo_mid_point_ms = 1.5

deflect_90_in_ms = 1

period_in_ms = 1000 / pwm_frequency
pulse_steps = 4096
steps_per_ms = pulse_steps / period_in_ms

steps_per_degree = (deflect_90_in_ms * steps_per_ms) / 90
servo_mid_point_steps = servo_mid_point_ms * steps_per_ms

def convert_degrees_to_steps(position): 
    return int(servo_mid_point_steps + (position * steps_per_degree))

servo_channels = (0,)

def turn_off_servos():
    for channel in servo_channels:
        pwm.setPWM(channel, 0, 4096)

atexit.register(turn_off_servos)


# atexit.register(pwm.setPWM, 0, 0, 4096)


while True: 
    position = int(input("Type your position in degrees (90 to -90, 0 is middle): "))
    for channel in servo_channels:
        end_step = convert_degrees_to_steps(position)
        pwm.setPWM(channel, 0, end_step)
