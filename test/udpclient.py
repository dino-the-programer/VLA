import socket

# Define server address and port
server_address = ('192.168.1.3', 9999)
message = b'Hello, Server!'

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Send data
    for i in range(1000):
        client_socket.sendto(message, server_address)
    
    # Receive response
        # data, server = client_socket.recvfrom(1024)
        # print(f'Received: {data.decode()}')
except Exception as e:
    print(e)
finally:
    client_socket.close()
