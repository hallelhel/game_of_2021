'''
● Looking for a server. You leave this state when you get an offer message.
● Connecting to a server. You leave this state when you successfully connect using TCP
● Game mode - collect characters and from the keyboard and send them over TCP. collect
data from the network and print it onscreen
'''
import socket, threading
import struct
import datetime, time
import getch
import time
host_name = '127.0.0.1'

# port for game
port = 13117

def Main():
    # client run for good
    while True:
        tcp_port = udp_protocol_on_client()
        if tcp_port != -1:
            # tcp connection
            tcp_protocol(tcp_port)


def tcp_protocol(tcp_port):
    try:
        # define tcp socket
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect to server from the address you got from udp
        tcp_socket.connect((host_name, tcp_port))
        # teams name to send to server
        team_name = "shay_hallel"
        # message sent to server
        tcp_socket.send(team_name.encode())
        # message received from server
        tcp_socket.settimeout(35)
        try:
            first_msg_from_tcp_server = tcp_socket.recv(1024).decode()
            print(first_msg_from_tcp_server)
            stop = datetime.datetime.now() + datetime.timedelta(seconds=10)
            try:
                while stop > datetime.datetime.now():
                    #s = "c"
                    play_touch = getch.getch()
                    # print(input("type"))
                    tcp_socket.send(play_touch.encode())
            except:
                print("client row 49 -- fail on play game")
            try:
                winner_message_from_server = tcp_socket.recv(1024).decode()
                print(winner_message_from_server)
                time.sleep(4)
            except:
                print("client waiting for winner message")
            # real_game end
        except:
            print("client problem while playing")
        # close the connection
        tcp_socket.close()
    except:
        print("client connection error to tcp server")

def udp_protocol_on_client():
    port_of_tcp = -1 # to stop the tcp
    # define udp socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,socket.IPPROTO_UDP)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # bind with the first port
    udp_socket.bind(("",port))
    print("Client started, waiting for offer requests...")
    valid_message = True
    #udp_socket.settimeout(20)
    try:
        while valid_message:
            buffer,address_server = udp_socket.recvfrom(1024)
            udp_message = struct.unpack('I B H', buffer)
            # chek ig the message in right type
            if udp_message[0] == 0xfeedbeef and udp_message[1] == 0x2:
                valid_message = False

            print (address_server[0])

        port_of_tcp = udp_message[2]
        global host_name
        host_name = address_server[0]
        #host_name = '127.0.0.1'
        #print(host_name)
        print(f"Received offer from {host_name}, attempting to connect...")
    except:
        print("can't connet to server udp")
    udp_socket.close()
    return port_of_tcp

if __name__ == '__main__':
    Main()