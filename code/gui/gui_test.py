import paramiko
import tkinter as tk
import os
from dotenv import load_dotenv

load_dotenv()

client = None

def establish_connection():
    # TODO globals are BAD
    global client
    # HOSTNAME = "a3a.local"
    PORT = 22
    # USERNAME = "shell"
    # PASSWORD = "pain"
    HOSTNAME = os.getenv("A3A_HOSTNAME")
    
    USERNAME = os.getenv("A3A_USERNAME")
    PASSWORD = os.getenv("A3A_PASSWORD")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
    client.connect(HOSTNAME, PORT, USERNAME, PASSWORD)

def execute_remote_command():
    global client
    # HOSTNAME = os.getenv("HOSTNAME")
    
    # USERNAME = os.getenv('USERNAME')
    # PASSWORD = os.getenv('PASSWORD')

    try: 
        stdin, stdout, stderr = client.exec_command('source /home/shell/defaultenv/bin/activate; python3 /home/shell/synced_servos.py')
        
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        if output:
            print("Output", output)
        if error:
            print("Error", error)
    
    except Exception as e:
        print("Connection Error", str(e))
    
def close_connection():
    global client
    client.close()

root = tk.Tk()
root.title("Remote Script Executor")

connect_button = tk.Button(root, text="establish_connection", command=establish_connection)
connect_button.pack()
execute_button = tk.Button(root, text="execute_remote_command", command=execute_remote_command)
execute_button.pack()
close_button = tk.Button(root, text="close_connection", command=close_connection)
close_button.pack()

root.mainloop()
