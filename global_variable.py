import socket, threading
from game import game
'''
    this class represent all global variables of the program        
'''
class globalV:
    host_name = socket.gethostbyname(socket.gethostname())
    lock_msg = threading.Lock()
    udp_prot_server = 13117
    tcp_prot_server = 4500
    lock_class_game = threading.Lock()
    lock_until_end = threading.Lock()
    real_game = game()
    max_types_per_player = 0