import socket
import cv2
import numpy as np

# Set up server socket
server_ip = '127.0.0.1'
server_port = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)  # Listen for incoming connections

print("Server listening on {}:{}".format(server_ip, server_port))

# Accept client connection
client_socket, client_address = server_socket.accept()
print("Client connected from:", client_address)

# Open the camera
camera = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = camera.read()  # Capture a frame from the camera

        if not ret:
            break

        # Serialize the image as bytes
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()

        # Send the image data to the client
        client_socket.send(len(img_bytes).to_bytes(4, byteorder='big'))  # Send image size first
        client_socket.send(img_bytes)
finally:
    camera.release()
    client_socket.close()
    server_socket.close()
