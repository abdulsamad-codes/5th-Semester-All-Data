import socket 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("192.168.170.128", 12345))
server.listen(1)
print("Server listening on port 12345")

conn, addr = server.accept()
print("Connection from", addr)
data = conn.recv(1024).decode()
print("Recieved: ", data)
conn.send("Hello from Server!".encode())
conn.close()
server.close()