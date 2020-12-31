import socket, threading
import datetime, time
import udp_protocol
import tcp_protocol
from game import game

class globalV:
    host_name = socket.gethostbyname(socket.gethostname())
    lock_msg = threading.Lock()
    udp_prot_server = 7002
    tcp_prot_server = 7000
    lock_class_game = threading.Lock()
    lock_until_end = threading.Lock()
    all_players = []
    real_game = game()

    # def __init__(self):
    #     self.host_name = socket.gethostbyname(socket.gethostname())
    #     global udp_prot_server
    #     udp_prot_server = 7002
    #     global tcp_prot_server
    #     tcp_prot_server = 7000
    #     global lock_class_game
    #     lock_class_game = threading.Lock()
    #     global lock_msg
    #     lock_msg = threading.Lock()
    #     global lock_until_end
    #     lock_until_end = threading.Lock()
    #     global all_players
    #     all_players = []
    #     global real_game
    #     real_game = game()