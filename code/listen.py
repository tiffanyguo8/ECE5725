import bluetooth
from gpiozero import Servo
import time
import struct
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)

GPIO.output(12, GPIO.HIGH)

servo_left = Servo(13)
servo_right = Servo(19)

# Create a Bluetooth socket and bind it to a port
server_socket1 = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket2 = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

#port = 1
server_socket1.bind(("", 1))
server_socket2.bind(("", 2))

# Listen for incoming Bluetooth connections
server_socket1.listen(1)
server_socket2.listen(2)

# Get the port number assigned to the socket
port1 = server_socket1.getsockname()[1]
port2 = server_socket2.getsockname()[1]

# Print the port number to the console
print("Waiting for connection on RFCOMM channel", port1)
print("Waiting for connection on RFCOMM channel", port2)

# Accept an incoming Bluetooth connection
client_socket1, client_info1 = server_socket1.accept()
print("Accepted connection from", client_info1)

client_socket2, client_info2 = server_socket2.accept()
print("Accepted connection from", client_info2)

# Convert gyroscope data (-90 to 90) if exceed, cap at max/min
def convert(gyro):
    if (gyro <= -90):
        return -1
    elif (gyro >= 90): 
        return 1
    else:
        return gyro / 90

# Receive data from the client
begin_time = time.time()
while time.time() < begin_time + 600:
    try:
        data_left = client_socket1.recv(1024)
        data_right = client_socket2.recv(1024)
        
        if data_left:
            print("Received left:", data_left)
            if(len(data_left) < 30):
                data_left = float(data_left)
                pwm_left = convert(data_left)
                servo_left.value = pwm_left
            
        if data_right:
            print("Received right:", data_right)
            if(len(data_right) < 30):
                data_right = float(data_right)
                pwm_right = convert(data_right)
                servo_right.value = pwm_right
            
    except bluetooth.btcommon.BluetoothError as error:
        print("Bluetooth connection error:", error)
        break

# Close the client socket and the server socket
client_socket1.close()
server_socket1.close()
client_socket2.close()
server_socket2.close()

GPIO.cleanup()
