import argparse
import robot
# from time import sleep

def print_separator():
        print("---------------------------------------------")

def print_done():
        print("… DONE")

# todo these are duplicates but fuck im tired just wanna see this work

a3a = robot.Robot()

# really?
def move_joint_incremental(joint, direction):
     a3a.move_joint_incremental(joint, direction)

def go_zero():
     a3a.go_zero()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Control the robot.")
    parser.add_argument("function", type=str, help="Function to execute: move_joint_incremental or go_zero")
    parser.add_argument("params", nargs="*", help="Parameters for the function")

    args = parser.parse_args()

    if args.function == "move_joint_incremental":
        if len(args.params) == 2:
            joint = int(args.params[0])
            direction = float(args.params[1])
            move_joint_incremental(joint, direction)
        else:
            print("Error: 'move_joint_incremental' requires 2 parameters: joint (int) and direction (float).")

    elif args.function == "go_zero":
        go_zero()

    else:
        print(f"Error: Unknown function '{args.function}'")


main_menu = """
1.  HOME
2.  JOG
3.  INCR JOG
4.  SET INCR JOG
5.  STATUS
6.  SET ACTIVE JOINT
7.  ZERO
8.  CAL SYS

> 
"""

# while True:
#     ch = int(input(main_menu))
#     if ch == 1:
#         print_separator()
#         rafs_3a.go_home()
#         print_separator()
#     elif ch == 2:
#         # joint_ch = input("1.\tJ1\n2.\tJ2\n3.\tJ3")
#         # rafs_3a.set_active_joint(rafs_3a.joint_selection(joint_ch))
#         pass
#     elif ch == 3:
#         while True:
#             print_separator()
#             ch = int(input("1.\t+\n2.\t-\n\n> "))
#             if ch == 0:
#                 break
            
#             if ch == 1: change = rafs_3a.incremental_jog
#             elif ch == 2: change = -rafs_3a.incremental_jog
#             # if rafs_3a.stroke_end(new_position):
#             #     print("STROKE END")
#             #     continue
#             rafs_3a.move_joint_relative(rafs_3a.active_joint['index'], change)
#             print_separator()
#     elif ch == 4:
#         print_separator()
#         rafs_3a.set_incremental_jog(int(input("Enter value:\n\n> ")))
#         print_separator()
#     elif ch == 5:
#         print_separator()
#         rafs_3a.show_status()
#         print_separator()
#     elif ch == 6:
#         print_separator()
#         rafs_3a.set_active_joint(int(input("1.\tJ1\n2.\tJ2\n3.\tJ3\n\n> "))-1)
#         print_separator()
#     elif ch == 7:
#         print_separator()
#         rafs_3a.go_zero()
#         print_separator()
#     elif ch == 8:
#         print_separator()
#         rafs_3a.go_cal_sys()
#         print_separator()

        
        


