import tkinter as tk
from ssh_manager import SSHClientManager

ssh_manager = SSHClientManager()

root = tk.Tk()
root.title("A3A")

connect_button = tk.Button(root, text="Establish Connection", command=ssh_manager.establish_connection)
connect_button.pack()


# this whole thing is ugly as sin

execute_button = tk.Button(root, text="J1 -5", command=lambda: ssh_manager.execute_remote_command('robot_obj_test.py move_joint_incremental 0 -1'))
execute_button.pack()
execute_button = tk.Button(root, text="J1 +5", command=lambda: ssh_manager.execute_remote_command('robot_obj_test.py move_joint_incremental 0 1'))
execute_button.pack()

execute_button = tk.Button(root, text="J2 -5", command=lambda: ssh_manager.execute_remote_command('robot_obj_test.py move_joint_incremental 1 -1'))
execute_button.pack()
execute_button = tk.Button(root, text="J2 +5", command=lambda: ssh_manager.execute_remote_command('robot_obj_test.py move_joint_incremental 1 1'))
execute_button.pack()

execute_button = tk.Button(root, text="J3 -5", command=lambda: ssh_manager.execute_remote_command('robot_obj_test.py move_joint_incremental 2 -1'))
execute_button.pack()
execute_button = tk.Button(root, text="J3 +5", command=lambda: ssh_manager.execute_remote_command('robot_obj_test.py move_joint_incremental 2 1'))
execute_button.pack()

execute_button = tk.Button(root, text="zero", command=lambda: ssh_manager.execute_remote_command('robot_obj_test.py go_zero'))
execute_button.pack()


close_button = tk.Button(root, text="Close Connection", command=ssh_manager.close_connection)
close_button.pack()

root.mainloop()
