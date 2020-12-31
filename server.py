import socket, threading
import datetime, time
import udp_protocol
import tcp_protocol
import global_variable
'''
    this class represent the server side       
'''

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def Main():
    while True:
        # global lock_msg
        # global lock_until_end
        # global real_game

        global_variable.globalV.lock_msg.acquire()
        global_variable.globalV.lock_until_end.acquire()
        udpthread = udp_protocol.udp_protocol()
        #print('\033[93m' + "udpThred start" + bcolors.ENDC)
        udpthread.start()
        tcpthread = tcp_protocol.tcp_protocol()
        #print("tcp thread start")
        tcpthread.start()
        tcpthread.join(10)
        udpthread.join(10)
        #print("udp/tcp thread finished")
        # if (len(all_players) != 0):
        # groupsMsg = game1.getGroupsMsg()
        global_variable.globalV.lock_msg.release()  # start real_game
        time.sleep(12)
        print("real_game Finished")
        global_variable.globalV.lock_until_end.release()
        time.sleep(10)
        global_variable.globalV.real_game.init_game()

        # else:
        #     lock_msg.release()
        #     lock_until_end.release()

    # close all the all_players
    # reset real_game

'''
    this class represent the threads connection        
'''
class threads_client_on_server(threading.Thread):
    # groupName = ""
    # clientname = ""

    def __init__(self, client_address, client_socket):
        threading.Thread.__init__(self)
        self.client_address = client_address
        self.client_socket = client_socket
        self.group_name = " "
        self.client_name = " "

    '''
        run function for the threads      
    '''
    def run(self):
        self.client_socket.settimeout(40)  # case no message received
        data = self.client_socket.recv(2048)
        self.client_name = data.decode()
        self.group_name = global_variable.globalV.real_game.addNewGroup(self.client_name)
        while (global_variable.globalV.lock_msg.locked()):
            time.sleep(0.01)
        self.message_to_start()
        # if not val:#player is not playing
        #
        #     return
        while (global_variable.globalV.lock_until_end.locked()):
            time.sleep(0.01)
        val = self.message_score()
        if not val:
            return

    '''
          function initialize the game      
    '''
    def message_to_start(self):
        try:
            msg = '\033[95m' + 'welcome to the play of 2021.\n' + bcolors.ENDC + bcolors.HEADER + bcolors.OKBLUE + bcolors.OKCYAN  + bcolors.ENDC + '\n'
            groups_msg = '\033[94m' + global_variable.globalV.real_game.get_group() + bcolors.ENDC
            start_msg = msg + groups_msg + bcolors.OKGREEN + '\nStart pressing keys on your keyboard as fast as you can!!\n' + bcolors.ENDC
            self.client_socket.send(start_msg.encode())

            counter_for_play = 0
            then = datetime.datetime.now() + datetime.timedelta(seconds=10)
            try:
                while then > datetime.datetime.now():
                    time.sleep(0.01)
                    self.client_socket.settimeout(10)
                    if self.client_socket.recv(1024):
                        counter_for_play += 1
            except:
                print("server didnt get typing")
                return False
            print(counter_for_play)
            print(self.group_name)
            global_variable.globalV.real_game.sum_score(counter_for_play, self.group_name)

        except:
            print("server client lost connection")
            return False

    def message_score(self):
        try:
            # game over message
            msg = bcolors.WARNING + bcolors.BOLD + global_variable.globalV.real_game.calc_total() + bcolors.ENDC
            self.client_socket.send(msg.encode())
        except:
            print("server client connection lost")
            return False

if __name__ == '__main__':
    Main()

