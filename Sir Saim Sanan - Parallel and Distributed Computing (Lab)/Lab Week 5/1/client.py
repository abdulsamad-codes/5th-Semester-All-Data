import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("192.168.170.128", 12345))
client.send("Hello from client!".encode())
response = client.recv(1024).decode()
print("Server response:", response)
client.close()