import socket
import cv2
import numpy as np

# Set up client socket
server_ip = '127.0.0.1'
server_port = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# OpenCV window to display the livestreamed images
cv2.namedWindow("Livestream", cv2.WINDOW_NORMAL)

try:
    while True:
        # Receive image size first
        img_size = int.from_bytes(client_socket.recv(4), byteorder='big')

        # Receive image data
        img_data = b""
        while len(img_data) < img_size:
            chunk = client_socket.recv(img_size - len(img_data))
            if not chunk:
                break
            img_data += chunk

        # Convert image data to numpy array
        img_array = np.frombuffer(img_data, dtype=np.uint8)

        # Decode image array and display
        img = cv2.imdecode(img_array, flags=cv2.IMREAD_COLOR)
        cv2.imshow("Livestream", img)
        
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cv2.destroyAllWindows()
    client_socket.close()
