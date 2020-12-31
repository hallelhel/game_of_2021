'''
● Looking for a server. You leave this state when you get an offer message.
● Connecting to a server. You leave this state when you successfully connect using TCP
● Game mode - collect characters and from the keyboard and send them over TCP. collect
data from the network and print it onscreen
'''
import socket, threading
import struct
import datetime, time
# import getch
import multiprocessing

import time
host = '127.0.0.1'

# Define the port on which you want to connect
port = 13117
port = 7002
tuching = True
def Main():
    continueask = True
    while continueask:
        Tcp_Port = udpState()
        if Tcp_Port != 0:
            tcp_protocol(Tcp_Port)
        global tuching
        tuching = True
        # if (input("continue? y/n") == 'n'):
        #     continueask = False


def tcp_protocol(tcp_port):
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to server on local computer
        tcp_socket.connect((host, tcp_port))
        # message you send to server
        team_name = "shay_hallel"
        # message sent to server
        tcp_socket.send(team_name.encode())
        # messaga received from server
        tcp_socket.settimeout(35)
        try:
            first_msg_from_tcp_server = tcp_socket.recv(1024).decode()
            print(first_msg_from_tcp_server)
            then = datetime.datetime.now() + datetime.timedelta(seconds=10)
            try:
                while then > datetime.datetime.now():
                    s = "c"
                    #tosend = getch.getch()
                    print(input("type"))
                    tcp_socket.send(s.encode())
            except:
                print("fail in getting tuch func")
            try:
                winner = tcp_socket.recv(1024).decode()
                print(winner)
                time.sleep(4)
            except:
                print("client line 87 --- waiting for winner message")
            # real_game end
        except:
            print("client line 90 --- problem while playing")
        # close the connection
        tcp_socket.close()
    except:
        print("client line 94 --- connection error to tcp server")

def udpState():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    TCP_PORT = 0
    udp_socket.bind(("",port))
    print("Client started, waiting for offer requests...")
    valid_message = True
    #udp_socket.settimeout(20)
    try:
        while valid_message:
            buffer,address = udp_socket.recvfrom(1024)
            unPackMsg = struct.unpack('I B H', buffer)
            if unPackMsg[0] == 0xfeedbeef and unPackMsg[1] == 0x2:
                valid_message = False
            #test with our own server
            print (address[0])
            # if address[0] != '192.168.1.18':
            #     print("not good offer")
            #     valid_message = True
            # else:
            #     print("goood offer")
            #     TCP_PORT = unPackMsg[2]
            #     print(TCP_PORT)
        TCP_PORT = unPackMsg[2]
        global host
        host = address[0]
        #host = '127.0.0.1'
        print(host)
        print(f"Received offer from {host}, attempting to connect...")
    except:
        print("can't connet to server udp")
    udp_socket.close()
    return TCP_PORT

if __name__ == '__main__':
    Main()