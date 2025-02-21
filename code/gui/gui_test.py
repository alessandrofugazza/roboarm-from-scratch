import tkinter as tk
from ssh_manager import SSHClientManager

ssh_manager = SSHClientManager()

root = tk.Tk()
root.title("Remote Script Executor")

connect_button = tk.Button(root, text="Establish Connection", command=ssh_manager.establish_connection)
connect_button.pack()
execute_button = tk.Button(root, text="Execute Remote Command", command=lambda: ssh_manager.execute_remote_command('source /home/shell/defaultenv/bin/activate; python3 /home/shell/synced_servos.py'))
execute_button.pack()
close_button = tk.Button(root, text="Close Connection", command=ssh_manager.close_connection)
close_button.pack()

root.mainloop()
