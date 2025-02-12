from Raspi_MotorHAT.Raspi_PWM_Servo_Driver import PWM 
import atexit
from time import sleep
import math
# from numpy import arange

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

servo_channels = (13, 15)
# servo_channels = [0, 2]

def turn_off_servos():
    # pwm.setPWM(servo_channel, 0, 4096)
    for channel in servo_channels:
        pwm.setPWM(channel, 0, 4096)

atexit.register(turn_off_servos)


# atexit.register(pwm.setPWM, 0, 0, 4096)


target_positions = [60, 60]

# step_delay = 0.01

# for servo_channel in servo_channels:
#     pwm.setPWM(servo_channel, 0, convert_degrees_to_steps(0))

pwm.setPWM(servo_channels[0], 0, convert_degrees_to_steps(-80))
pwm.setPWM(servo_channels[1], 0, convert_degrees_to_steps(10))

sleep(1)

current_positions = [-80 ,10]

DEGREES_PER_STEP = 2

diffs = []

for i in range(len(servo_channels)):
    diffs.append(abs(target_positions[i] - current_positions[i]))

steps_needed = max(diffs) / DEGREES_PER_STEP

deg_steps = []

for i in range(len(servo_channels)):
    deg_steps.append((diffs[i] / steps_needed))

directions = []
for i in range(len(servo_channels)):
    directions.append(1 if target_positions[i] > current_positions[i] else -1)

print(current_positions[0] + deg_steps[0] * directions[0])
print(current_positions[1] + deg_steps[1] * directions[1])

for _ in range(int(steps_needed)):
    for index in range(len(servo_channels)):
        current_positions[index] += deg_steps[index] * directions[index]
        pwm.setPWM(servo_channels[index], 0, convert_degrees_to_steps(current_positions[index]))
    sleep(0.1)

for index in range(len(servo_channels)):
    pwm.setPWM(servo_channels[index], 0, convert_degrees_to_steps(target_positions[index]))


# deg_per_sec = 45

# frames_per_90 = 50
# radians_per_frame = (2 * math.pi) / frames_per_90

# while True: 









    
# steps = []
# directions = []

# target_position = int(input("Type your position in degrees (90 to -90, 0 is middle): "))
# target_position2 = target_position/2
# target_positions = [target_position, target_position2]

# current_time = 0 

# max_angle = max(target_positions)

# total_time = max_angle/frames_per_90

# frame_number = current_time % frames_per_90






# for i, channel in enumerate(servo_channels):
#     delta = convert_degrees_to_steps(target_positions[i]) - convert_degrees_to_steps(current_positions[i])
#     steps.append(abs(delta))
#     directions.append(1 if delta > 0 else -1)

# max_steps = max(steps)
# print(max_steps)
# print(steps)
# print(directions)



# for step in range(max_steps):

#     for i, channel in enumerate(servo_channels):

#         if step < steps[i]:
#             current_positions[i] += directions[i]
#             pwm_value = convert_degrees_to_steps(current_positions[i])
#             pwm.setPWM(channel, 0, pwm_value)

#     sleep(step_delay)

# Ensure the final position is set
# for i, channel in enumerate(servo_channels):
#     pwm_value = convert_degrees_to_steps(target_positions[i])
#     pwm.setPWM(channel, 0, pwm_value)
#     current_positions[i] = target_positions[i]

