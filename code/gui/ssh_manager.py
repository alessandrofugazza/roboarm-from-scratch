import paramiko
import os
from dotenv import load_dotenv

load_dotenv()

class SSHClientManager:
    def __init__(self):
        self.hostname = os.getenv("A3A_HOSTNAME")
        self.port = 22
        self.username = os.getenv("A3A_USERNAME")
        self.password = os.getenv("A3A_PASSWORD")
        self.client = None

    def establish_connection(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.hostname, self.port, self.username, self.password)
        print("Connection established")

    def execute_remote_command(self, command):
        try:
            stdin, stdout, stderr = self.client.exec_command("source /home/shell/defaultenv/bin/activate; python3 /home/shell/" + command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            if output:
                print("Output:", output)
            if error:
                print("Error:", error)
        except Exception as e:
            print("Connection Error:", str(e))

    def close_connection(self):
        if self.client:
            self.client.close()
            print("Connection closed")
