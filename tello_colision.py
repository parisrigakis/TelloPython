import socket
import time
from time import sleep

INTERVAL = 0.05

def giveNum(state, measurement):
	index = 0
	for word in state:
		index += 1
		if word == measurement:
			return float(state[index])
			#return index

#index_for_tof: 19



if __name__ == "__main__":

    host = ''
    port = 9000
    locaddr = (host,port) 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(locaddr)

    local_ip = ''
    local_port = 8890
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd
    socket.bind((local_ip, local_port))

    tello_ip = '192.168.10.1'
    tello_port = 8889
    tello_adderss = (tello_ip, tello_port)

    sock.sendto('command'.encode('utf-8'), tello_adderss)
    start = time.time()
    sleep(2)
    sock.sendto('takeoff'.encode('utf-8'), tello_adderss)
    try:
        index = 0
        while True:
            index += 1
            response, ip = socket.recvfrom(1024)
            if response.decode(encoding="utf-8") == 'ok':
                continue
            out = response.decode(encoding="utf-8").replace(';', '\n')
            out = out.replace(':', ' ')
            out = 'Tello State:\n' + out
            state = out.split()
            tof = giveNum(state, 'tof')
            agx = giveNum(state, 'agx')
            agy = giveNum(state, 'agy')
            print(tof,agy)
            #sleep(INTERVAL)
            if agx < -100:
                sock.sendto('back 40'.encode('utf-8'), tello_adderss)
            if agx > 100:
                sock.sendto('forward 40'.encode('utf-8'), tello_adderss)
            if agy > 100:
                sock.sendto('right 40'.encode('utf-8'), tello_adderss)
            if agy < -100:
                sock.sendto('left 40'.encode('utf-8'), tello_adderss)
            if (tof - 100) < 0:
                if abs(tof - 100) > 20:
                    strings = 'up ' + str(abs(tof - 100))
                    sock.sendto(strings.encode('utf-8'), tello_adderss)
            else:
                if abs(tof - 100) > 20:
                    strings = 'down ' + str(abs(tof - 100))
                    sock.sendto(strings.encode('utf-8'), tello_adderss)
            if (time.time() - start) > 10:
                sock.sendto('command'.encode('utf-8'), tello_adderss)
                start = time.time()
    except KeyboardInterrupt:
        print ('\nExit . . .\n')
        sock.close
        socket.close





