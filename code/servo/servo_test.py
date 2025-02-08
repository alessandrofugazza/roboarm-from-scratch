from Raspi_MotorHAT.Raspi_PWM_Servo_Driver import PWM 
import atexit
import time

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

servo_channels = (0, 2, 4)
current_positions = [0, 0, 0]

def turn_off_servos():
    for channel in servo_channels:
        pwm.setPWM(channel, 0, 4096)

atexit.register(turn_off_servos)

def move_servo_slowly(channel, start_position, end_position, step_delay=0.01):
    start_step = convert_degrees_to_steps(start_position)
    end_step = convert_degrees_to_steps(end_position)
    step = 1 if end_step > start_step else -1

    for position in range(start_step, end_step, step):
        pwm.setPWM(channel, 0, position)
        time.sleep(step_delay)
    pwm.setPWM(channel, 0, end_step)

for channel in servo_channels:
    end_step = convert_degrees_to_steps(0)
    pwm.setPWM(channel, 0, end_step)



while True: 
    joint = int(input("select J"))
    if joint >= 1 and joint <= 3:
        position = int(input("select P"))
        if position >= -89 and position <= 89:
            move_servo_slowly(servo_channels[joint - 1], current_positions[joint-1], position)
            current_positions[joint-1] = position
        else:
            print("Invalid P")
    else:
        print("Invalid J")
    print("done")
    # position = int(input("Type your position in degrees (90 to -90, 0 is middle): "))
    # for channel in servo_channels:
    #     end_step = convert_degrees_to_steps(position)
    #     pwm.setPWM(channel, 0, end_step)
