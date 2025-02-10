import robot
# from time import sleep

rafs_3a = robot.Robot()

while True:
    ch = int(input("1.\tHOME\n2.\tJOG\n3.\tINCR JOG\n4.\tSET INCR JOG\n5.\tSTATUS\n6.\tSET ACTIVE JOINT\n7.\tZERO"))
    if ch == 1:
        rafs_3a.go_home()
    elif ch == 2:
        # joint_ch = input("1.\tJ1\n2.\tJ2\n3.\tJ3")
        # rafs_3a.set_active_joint(rafs_3a.joint_selection(joint_ch))
        pass
    elif ch == 3:
        while True:
            ch = int(input("1.\t+\n2.\t-"))
            if ch == 0:
                break
            direction = 1 if ch == 1 else -1
            current_position = rafs_3a.joints[rafs_3a.active_joint]['current_position']
            new_position = current_position + direction * rafs_3a.incremental_jog
            # if rafs_3a.stroke_end(new_position):
            #     print("STROKE END")
            #     continue
            rafs_3a.move_joint_relative(rafs_3a.active_joint, new_position)
    elif ch == 4:
        rafs_3a.set_incremental_jog(int(input("Enter value: ")))
    elif ch == 5:
        rafs_3a.show_status()
    elif ch == 6:
        rafs_3a.set_active_joint(rafs_3a.joint_selection(input("1.\tJ1\n2.\tJ2\n3.\tJ3")))
    elif ch == 7:
        rafs_3a.go_zero()
        
        


