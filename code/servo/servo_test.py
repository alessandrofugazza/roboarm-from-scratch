from Raspi_MotorHAT.Raspi_PWM_Servo_Driver import PWM 
import atexit
from time import sleep

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
        sleep(step_delay)
    pwm.setPWM(channel, 0, end_step)

def go_home():
    print("GRAB THE FUCKING BASE")
    sleep(1)
    print("3")
    sleep(1)
    print("2")
    sleep(1)
    print("1")
    sleep(1)
    
    for channel in servo_channels:
        end_step = convert_degrees_to_steps(0)
        pwm.setPWM(channel, 0, end_step)

    current_positions = [0, 0, 0]



def user_wants_to_go_back(input):
    return input.lower() == 'b'

def is_stroke_end(position):
    return position > 89 or position < -89

print("-----------------")
print("3A ROBOARM FROM SCRATCH Menu Driven Interface v0.1")
print("WELCOME")
print("EXPECT BUGS")
print("-----------------")


while True: 
    choice = int(input(("1.\tTest single joints\n2.\tCreate point to point program.\n3.\tHome\nInput 'b' at any time to go back\n> ")))
    if choice == 1:
        print("Test single joints")
        print("-----------------")
        while True:
            input = input("select J\n> ")
            # if user_wants_to_go_back(input):
            #     break
            joint = int(input)
            if joint >= 1 and joint <= 3:
                choice = input("select P\n> ")
                # if user_wants_to_go_back(input):
                #     break
                position = int(choice)
                if position >= -89 and position <= 89:
                    move_servo_slowly(servo_channels[joint - 1], current_positions[joint-1], position)
                    current_positions[joint-1] = position
                else:
                    print("Invalid P")
            else:
                print("Invalid J")
            print("done")
    elif choice == 2:
        print("GOOD CHOICE")
        print("-----------------")
        program_positions = []
        go_home()

        while True:
            choice = input("1.\tJ1 +10\n2.\tJ1 -10\n3.\tJ2 +10\n4.\tJ2 -10\n5.\tJ3 +10\n6.\tJ3 -10\n7.\tREC\n8.\t SHOW PROGRAM\n9.\tRUN PROGRAM\n> ")
            # if user_wants_to_go_back(input):
            #     break
            choice = int(choice)
            if choice == 1:
                if is_stroke_end(current_positions[0] + 10):
                    print("STROKE END")
                    continue
                move_servo_slowly(servo_channels[0], current_positions[0], current_positions[0] + 10)
                current_positions[0] += 10
            elif choice == 2:
                if is_stroke_end(current_positions[0] - 10):
                    print("STROKE END")
                    continue
                move_servo_slowly(servo_channels[0], current_positions[0], current_positions[0] - 10)
                current_positions[0] -= 10
            elif choice == 3:
                if is_stroke_end(current_positions[1] + 10):
                    print("STROKE END")
                    continue
                move_servo_slowly(servo_channels[1], current_positions[1], current_positions[1] + 10)
                current_positions[1] += 10
            elif choice == 4:
                if is_stroke_end(current_positions[1] - 10):
                    print("STROKE END")
                    continue
                move_servo_slowly(servo_channels[1], current_positions[1], current_positions[1] - 10)
                current_positions[1] -= 10
            elif choice == 5:
                if is_stroke_end(current_positions[2] + 10):
                    print("STROKE END")
                    continue
                move_servo_slowly(servo_channels[2], current_positions[2], current_positions[2] + 10)
                current_positions[2] += 10
            elif choice == 6:
                if is_stroke_end(current_positions[2] - 10):
                    print("STROKE END")
                    continue
                move_servo_slowly(servo_channels[2], current_positions[2], current_positions[2] - 10)
                current_positions[2] -= 10
            elif choice == 7:
                program_positions.append(current_positions[:])
                print("Position recorded:", current_positions)
                print("Program:")
                [print(p) for p in program_positions]
            elif choice == 8:
                print("Program:")
                [print(p) for p in program_positions]
            elif choice == 9:
                for position in program_positions:
                    # move_servo_slowly(servo_channels[0], current_positions[0], position[0])
                    # move_servo_slowly(servo_channels[1], current_positions[1], position[1])
                    # move_servo_slowly(servo_channels[2], current_positions[2], position[2])
                    for index, j_pos in enumerate(position):
                        end_step = convert_degrees_to_steps(j_pos)
                        pwm.setPWM(servo_channels[index], 0, end_step)
                    current_positions = position
                    sleep(1)
            
    elif choice == 3:
        go_home()
    
    # position = int(input("Type your position in degrees (90 to -90, 0 is middle): "))
    # for channel in servo_channels:
    #     end_step = convert_degrees_to_steps(position)
    #     pwm.setPWM(channel, 0, end_step)
