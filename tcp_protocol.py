import global_variable
import socket, threading
import global_variable
import server

'''
    this class for tcp connection - after udp connection success
    to get the tcp address from server          
'''
class tcp_protocol(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.tcp()

    def tcp(self):
        try:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tcp_socket.bind((global_variable.globalV.host_name, global_variable.globalV.tcp_prot_server))
            tcp_socket.settimeout(10)
            try:
                while True:
                    tcp_socket.listen(10)
                    client_socket, client_address = tcp_socket.accept()
                    print("tcp_protocol client try connect")

                    client_thread = server.threads_client_on_server(client_address, client_socket)
                    client_thread.start()
                    # globalVariable.globalV.all_players.append(newthread)
            except:
                tcp_socket.close()
                #print("tcp connection close")
        except:
            print("tcp protocol exception")
