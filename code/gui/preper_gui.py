import tkinter as tk
from tkinter import ttk
from ssh_manager import SSHClientManager

# TODO use iteration to add guiobjects

ssh_manager = SSHClientManager()


# def print_status():
#     ssh_manager.send_command("a3a.show_status()")


root = tk.Tk()
root.title("A3A")

incremental_jog = tk.StringVar(value="10") # get this from a3a

incremental_jog_label = ttk.Label(root, text="Incremental Jog: ")
incremental_jog_label.pack()
incremental_jog_entry = ttk.Entry(root, width=2, textvariable=incremental_jog)
incremental_jog_entry.pack()

execute_button = ttk.Button(root, text="Update Incremental Jog", command=lambda: ssh_manager.send_command(f'a3a.set_incremental_jog({incremental_jog.get()})'))
execute_button.pack()

execute_button = ttk.Button(root, text="STATUS", command=lambda: ssh_manager.send_command('a3a.show_status()'))
execute_button.pack()



execute_button = ttk.Button(root, text=f"J1 -{incremental_jog.get()}", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(0, -1)'))
execute_button.pack()
execute_button = ttk.Button(root, text=f"J1 +{incremental_jog.get()}", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(0, 1)'))
execute_button.pack()

execute_button = ttk.Button(root, text=f"J2 -{incremental_jog.get()}", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(1, -1)'))
execute_button.pack()
execute_button = ttk.Button(root, text=f"J2 +{incremental_jog.get()}", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(1, 1)'))
execute_button.pack()

execute_button = ttk.Button(root, text=f"J3 -{incremental_jog.get()}", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(2, -1)'))
execute_button.pack()
execute_button = ttk.Button(root, text=f"J3 +{incremental_jog.get()}", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(2, 1)'))
execute_button.pack()

execute_button = ttk.Button(root, text="zero", command=lambda: ssh_manager.send_command('a3a.go_zero()'))
execute_button.pack()

connect_button = ttk.Button(root, text="Establish Connection", command=ssh_manager.establish_connection)
connect_button.pack(side="left")

close_button = ttk.Button(root, text="Close Connection", command=ssh_manager.close_connection)
close_button.pack(side="right")

root.mainloop()
