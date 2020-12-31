import threading
import time
import socket
import struct
import datetime
import global_variable

class udp_protocol(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.udp()

    def udp(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # pack the udp format with struct
        udp_offer_msg = struct.pack('I B H', 0xfeedbeef, 0x2, global_variable.globalV.tcp_prot_server)

        print(f"Server started,listening on IP address {global_variable.globalV.host_name}")
        # udp connection open for 10 sec
        stop = datetime.datetime.now() + datetime.timedelta(seconds=10)
        while stop > datetime.datetime.now():
            udp_socket.sendto(udp_offer_msg, ('172.1.0', global_variable.globalV.udp_prot_server))
            #udp_socket.sendto(udp_offer_msg, ('<broadcast>', global_variable.globalV.udp_prot_server))
            time.sleep(1)

        # closing the udp thread after 10 seconds of offering messages.
        udp_socket.close()