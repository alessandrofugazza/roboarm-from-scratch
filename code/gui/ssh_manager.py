import time
import paramiko
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

class SSHClientManager:
    def __init__(self):
        self.hostname = os.getenv("A3A_HOSTNAME")
        self.port = 22
        self.username = os.getenv("A3A_USERNAME")
        self.password = os.getenv("A3A_PASSWORD")
        self.client = None
        self.shell = None

    def establish_connection(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.hostname, self.port, self.username, self.password)
        self.shell = self.client.invoke_shell()
        print("Interactive shell established")
        self.send_command("source /home/shell/defaultenv/bin/activate")
        self.send_command("python3 -i")
        self.send_command("import robot")
        self.send_command("a3a = robot.Robot()")
        print("Robot instance created.")

    def get_data(self, command):
        if self.shell:
            self.shell.send(command + "\n")
            output = ""
            while not self.shell.recv_ready():
                time.sleep(0.1)  # Polling until output is ready
            while self.shell.recv_ready():
                output += self.shell.recv(4096).decode().strip()
            print(f"Raw output: {output}")  # Debug print to see the raw output
            # Regex to extract JSON block
            json_match = re.search(r'\{.*\}', output)
            if json_match:
                json_str = json_match.group()
                try:
                    data = json.loads(json_str)
                    print(f"Parsed Data: {data}")
                    return data
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {e}")
            else:
                print("No JSON found in output.")
        else:
            print("Shell not initialized.")
    
    def send_command(self, command):
        if self.shell:
            self.shell.send(command + "\n")
            output = ""
            while not self.shell.recv_ready():
                time.sleep(0.1)  # Polling until output is ready
            while self.shell.recv_ready():
                output += self.shell.recv(4096).decode().strip()
            print(output)
            return output
        else:
            print("Shell not initialized.")

    def close_connection(self):
        if self.shell:
            self.send_command("exit()") 
        if self.client:
            self.client.close()
            print("Connection closed.")

