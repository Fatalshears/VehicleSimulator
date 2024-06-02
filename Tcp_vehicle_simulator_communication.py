import socket
import struct
import time

#Command
# 1/ StartSimulation
# 2/ SetSpeed_x -> x in km/h
# 3/ SetSteering_x -> x in rad, range -3.14 to 3.14
# 4/ SetBrake_x -> x range 0..1
# 5/ SetEgoPosition_x_y_rot -> x in m, y in m, z in degree
# 6/ SpawnObject_x -> x in [JaguarDaimlerV8, RamTRX, MotorbikeFatBoy90, Bicycle, PedestrianMan]
# 7/ SetObjectPosition_id_x_y_rot -> id is object spawn order, first spawn is 0, second spawn is 1, etc., 255 is invalid
# 8/ EnableControlObject_id_x_y_z -> id is object spawn order, x is desired speed in km/h, y is desired steering in rad, z is brake in 0..1
# 9/ DisableControlObject -> free all controlled objects
# 10/ SetAcceleration_x -> x in m/s2

# Data encoding rule
# Byte no.1 - Data type (1 - float, 2 - integer, 3 - string)
# Byte no.2 - Data length in number of bytes
# Byte no.3 - Data tag (1 - ego speed, 2 - ego gear, 3 - engine RPM, 4 - master cylinder pressure)
# Remaining bytes - Value

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 7000  # Port to listen on (non-privileged ports are > 1023)

doOnce = True
doOnce_1 = True
doOnce_2 = True
brake_enable = False
brake_disable = False
step_0_success = False

def decode_bytes(received_bytes):
    print ("")
    print ("Start")
    if (request[2] == 1):
        print("Ego Speed")
    if (request[2] == 2):
        print("Ego Gear")

    if(request[0] == 1):
        end = 3+request[1] 
        speed = struct.unpack('f', request[3:end])[0]
        print(speed)


    if (request[0] == 2):
        end = 3+request[1] 
        print(int.from_bytes(request[3:end], byteorder='little'))
    print ("End")
    print ("")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
# accept incoming connections
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    while True:
        if doOnce:
            response = "StartSimulation".encode("utf-8") 
            client_socket.send(response)
            doOnce = False
            time.sleep(4)
            response = "SpawnObject_RamTRX".encode("utf-8") 
            client_socket.send(response)
            time.sleep(1)
            response = "SetObjectPosition_0_30_-6_10".encode("utf-8") # set object id 0 at 30m in x direction, -6m in y direction, rotation around z is 10 degree
            client_socket.send(response)
            time.sleep(3) 

        try:
            request = client_socket.recv(1024)
            decode_bytes(request)
        except Exception as e:
            pass

        if doOnce_1:
            response = "SetSpeed_45".encode("utf-8") # set ego speed 60km/h
            client_socket.send(response)
            time.sleep(1)
            response = "EnableControlObject_0_50_0_0".encode("utf-8") # set object id 0 with speed 50km/h, no steering, no brake
            client_socket.send(response)
            doOnce_1 = False



