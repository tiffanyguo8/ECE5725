# This is the final one :)

import bluetooth
import time
from mpu6050 import mpu6050
import numpy as np

#begin_time = time.time()
#while time.time() < begin_time + 120:
#    pass
#time.sleep(120)

sensor = mpu6050(0x68)

server_address = "DC:A6:32:B4:12:B4"

client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_socket.connect((server_address,1))

begin_time = time.time()
while time.time() < begin_time + 180:
    try:
        accel_data = sensor.get_accel_data()
        gyro_data = sensor.get_gyro_data()
        temp = sensor.get_temp()
    
        #data = input()
        pitch = np.arctan2(accel_data['y'], accel_data['z']) * 180/np.pi
        print(pitch)
        data = pitch
        client_socket.send(str(data))
        #time.sleep(0.1)
        time.sleep(0.5)
    except bluetooth.btcommon.BluetoothError as error:
        print("Bluetooth connection error:", error)
        break
    
client_socket.close()
