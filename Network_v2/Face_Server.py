import socket
import time
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
pulseX = 350
pulseY = 350
print('Moving servo to original position.')
pwm.set_pwm(0, 0, pulseX)
pwm.set_pwm(15, 0, pulseY)

TCP_IP = 'raspberrypi.local'
TCP_PORT_x = 9982
TCP_PORT_y = TCP_PORT_x + 1
BUFFER_SIZE = 4096

print('Binding address to ', TCP_IP, ':', TCP_PORT_x)
xSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
xSocket.bind((TCP_IP, TCP_PORT_x))
xSocket.listen(1)
print('Binding Successful!')

print('Binding address to ', TCP_IP, ':', TCP_PORT_y)
ySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ySocket.bind((TCP_IP, TCP_PORT_y))
ySocket.listen(1)
print('Binding Successful!')

connX, addrX = xSocket.accept()
print('Connection address:', addrX)
connY, addrY = ySocket.accept()
print('Connection address:', addrY)

dataX = b'0'
dataY = b'0'

while 1:
    dataX = connX.recv(BUFFER_SIZE)
    dataY = connY.recv(BUFFER_SIZE)
    xCenter = int(dataX)
    yCenter = int(dataY)
    print("Received data:", xCenter, yCenter)
    if xCenter > 370:
        pulseX = pulseX - 10
        if pulseX < 150:
            pulseX = 150
            print("Face out of range")
        print("Turning left", pulseX)
        pwm.set_pwm(0, 0, pulseX)
    if xCenter < 270:
        pulseX = pulseX + 10
        if pulseX > 600:
            pulseX = 600
            print("Face out of range")
        print("Turning right", pulseX)
        pwm.set_pwm(0, 0, pulseX)

    if yCenter > 270:
        pulseY = pulseY - 10
        if pulseY < 250:
            pulse = 250
            print("Face out of range")
        print("Turning down", pulseY)
        pwm.set_pwm(15, 0, pulseY)
    if yCenter < 210:
        pulseY = pulseY + 10
        if pulseY > 450:
            pulseY = 450
            print("Face out of range")
        print("Turning up", pulseY)
        pwm.set_pwm(15, 0, pulseY)

    if xCenter == -1:
        break
    time.sleep(0.01)

xSocket.close()
ySocket.close()
