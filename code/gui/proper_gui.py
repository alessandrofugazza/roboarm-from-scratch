import threading
import tkinter as tk
from tkinter import ttk
from ssh_manager import SSHClientManager
from time import sleep


# TODO use iteration to add guiobjects
# TODO real time status feedback (convert steps to degrees)

ssh_manager = SSHClientManager()


# def print_status():
#     ssh_manager.send_command("a3a.show_status()")


root = tk.Tk()
root.geometry("900x900")
root.title("A3A")


def update_status_gui():
    status = ssh_manager.get_data("a3a.return_status()")  
    while not status:
        sleep(0.1)
        status = ssh_manager.get_data("a3a.return_status()") 
    
    if status:
        # incremental_jog.set(status.get('incremental_jog', 'N/A'))
        j1_position.set(status.get('j1', 'N/A'))
        j2_position.set(status.get('j2', 'N/A'))
        j3_position.set(status.get('j3', 'N/A'))
        j4_position.set(status.get('j4', 'N/A'))
        j5_position.set(status.get('j5', 'N/A'))
        j6_position.set(status.get('j6', 'N/A'))
    else:
        print("No status received.")
    
      # Schedule the function to run again after 500ms


incremental_jog = tk.StringVar(value="10") # get this from a3a
j1_position = tk.StringVar(value="0")
j2_position = tk.StringVar(value="-2")
j3_position = tk.StringVar(value="-6")
j4_position = tk.StringVar(value="135")
j5_position = tk.StringVar(value="0")
j6_position = tk.StringVar(value="0")
shitty_joint_positions = tk.StringVar(value="shitty")

incremental_jog_frame = ttk.Frame(root)
incremental_jog_frame.pack()

incremental_jog_label = ttk.Label(incremental_jog_frame, text="Incremental Jog: ")
incremental_jog_label.pack(ipadx=10, ipady=10, side="left")
incremental_jog_entry = ttk.Entry(incremental_jog_frame, width=2, textvariable=incremental_jog)
incremental_jog_entry.pack(side="right")



for i, joint in enumerate(['J1', 'J2', 'J3', 'J4', 'J5', 'J6'], start=1):
    frame = ttk.Frame(root, padding=(20, 10, 20, 0))
    frame.pack(fill="both")
    
    label = ttk.Label(frame, text=f"{joint}: ")
    label.pack(ipadx=10, ipady=10, side="left")
    
    entry = ttk.Entry(frame, width=3, textvariable=globals()[f'j{i}_position'])
    entry.pack(side="left")


execute_button = ttk.Button(root, text="Update Incremental Jog", command=lambda: ssh_manager.send_command(f'a3a.set_incremental_jog({incremental_jog.get()})'))
execute_button.pack()

def start_updating():
    while True:
        update_status_gui()
        sleep(0.1)

# LEARN THREADING
execute_button = ttk.Button(root, text="STATUS", command=lambda: threading.Thread(target=start_updating, daemon=True).start())
execute_button.pack()


frame = ttk.Frame(root)
frame.pack()

execute_button = ttk.Button(frame, text=f"J1 -", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(0, -1)'))
execute_button.grid(row=0, column=0)
execute_button = ttk.Button(frame, text=f"J1 +", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(0, 1)'))
execute_button.grid(row=0, column=1)

execute_button = ttk.Button(frame, text=f"J2 -", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(1, -1)'))
execute_button.grid(row=1, column=0)
execute_button = ttk.Button(frame, text=f"J2 +", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(1, 1)'))
execute_button.grid(row=1, column=1)

execute_button = ttk.Button(frame, text=f"J3 -", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(2, -1)'))
execute_button.grid(row=2, column=0)
execute_button = ttk.Button(frame, text=f"J3 +", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(2, 1)'))
execute_button.grid(row=2, column=1)

execute_button = ttk.Button(frame, text=f"J4 -", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(3, -1)'))
execute_button.grid(row=3, column=0)
execute_button = ttk.Button(frame, text=f"J4 +", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(3, 1)'))
execute_button.grid(row=3, column=1)

execute_button = ttk.Button(frame, text=f"J5 -", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(4, -1)'))
execute_button.grid(row=4, column=0)
execute_button = ttk.Button(frame, text=f"J5 +", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(4, 1)'))
execute_button.grid(row=4, column=1)

execute_button = ttk.Button(frame, text=f"J6 -", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(5, -1)'))
execute_button.grid(row=5, column=0)
execute_button = ttk.Button(frame, text=f"J6 +", command=lambda: ssh_manager.send_command('a3a.move_joint_incremental(5, 1)'))
execute_button.grid(row=5, column=1)

# frame = ttk.Frame(root).pack()

execute_button = ttk.Button(root, text="zero", command=lambda: ssh_manager.send_command('a3a.go_zero()'))
execute_button.pack()
execute_button = ttk.Button(root, text="home", command=lambda: ssh_manager.send_command('a3a.go_home()'))
execute_button.pack()

connect_button = ttk.Button(root, text="Establish Connection", command=ssh_manager.establish_connection)
connect_button.pack(side="left")

close_button = ttk.Button(root, text="Close Connection", command=ssh_manager.close_connection)
close_button.pack(side="right")


root.mainloop()

# Remove the redundant thread start
# threading.Thread(target=start_updating, daemon=True).start()
# threading.Thread(target=update_status_gui, daemon=True).start()