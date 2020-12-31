import gobalVariable
import socket, threading
import gobalVariable
import server
class tcp_protocol(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.tcp()

    def tcp(self):
        try:
            tcp_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tcp_soc.bind((gobalVariable.globalV.host_name, gobalVariable.globalV.tcp_prot_server))
            tcp_soc.settimeout(10)
            try:
                while True:
                    tcp_soc.listen(10)
                    client_socket, client_address = tcp_soc.accept()
                    print("tcp_protocol row 24 -- client try connect")

                    newthread = server.ClientThread(client_address, client_socket)
                    newthread.start()
                    # gobalVariable.globalV.all_players.append(newthread)
            except:
                tcp_soc.close()
                print("tcp_protocol row 29(timeout-end tcp connect time)")
        except:
            print("tcp_protocol row 31 exception 2")
