import socket
import struct
import time

#Command
# 1/ StartSimulation
# 2/ SetSpeed_x -> x in km/h
# 3/ SetSteering_x -> x in rad, range -3.14 to 3.14
# 4/ SetBrake_x -> x range 0..1
# 5/ SetEgoPosition_x_y_rot -> x in m, y in m, z in degree
# 6/ SpawnObject_x -> x in [JaguarDaimlerV8, RamTRX, MotorbikeFatBoy90, Bicycle, PedestrianMan, Dog]
# 7/ SetObjectPosition_id_x_y_rot -> id is object spawn order, first spawn is 0, second spawn is 1, etc., 255 is invalid
# 8/ EnableControlObject_id_x_y_z -> id is object spawn order, x is desired speed in km/h, y is desired steering in rad, z is brake in 0..1
# for characters (PedestrianMan, Dog): there is no brake implementation, if you want to stop a character, the only way is to set speed to 0
# for characters (PedestrianMan, Dog): don't use rotation to change movement direction, use desired steering instead
# 9/ DisableControlObject -> free all controlled objects
# 10/ SetAcceleration_x -> x in m/s2

# Data encoding rule

# First byte - Data tag 
#  1 - ego speed (float 4 bytes, km/h)
#  2 - ego gear (integer 4 bytes)
#  3 - ego engine RPM (float)
#  4 - ego master cylinder pressure (float, bar)
#  5 - ego longitudinal acceleration (float, m/s2)
#  6 - ego lateral acceleration (float, m/s2)
#  7 - ego yaw rate (float, deg/s)
# Remaining bytes - Value

# Exception
#  200 - object data
#         2nd byte: object ID
#         3rd byte: object type (2: Car, 3: Motorbike, 4: Truck, 5: Bus, 6: Bicycle, 7: Pedestrian)
#         4th-7th byte: dx relative to ego (m)
#         8th-11th byte: dy relative to ego
#         12th-15th byte: dz relative to ego
#         16th-19th byte: vx relative to ego (m/s)
#         20th-23rd byte: vy relative to ego
#         24th-27th byte: yaw angle relative to ego (deg)





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
    if (request[0] == 1):
        print("Ego Speed")
        speed = struct.unpack('f', request[1:5])[0]
        print(speed)
    if (request[0] == 2):
        print("Ego Gear")
        print(int.from_bytes(request[1:5], byteorder='little'))
        
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
            response = "SetObjectPosition_0_30_-6_5".encode("utf-8") # set object id 0 at 30m in x direction, -6m in y direction, rotation around z is 5 degree
            client_socket.send(response)
            time.sleep(3) 

        try:
            request = client_socket.recv(1024)
            decode_bytes(request)
        except Exception as e:
            break

        if doOnce_1:
            response = "SetSpeed_45".encode("utf-8") # set ego speed 45km/h
            client_socket.send(response)
            time.sleep(1)
            response = "EnableControlObject_0_50_0_0".encode("utf-8") # set object id 0 with speed 50km/h, no steering, no brake
            client_socket.send(response)
            doOnce_1 = False



