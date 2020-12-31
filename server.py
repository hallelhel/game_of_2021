import socket, threading
import datetime, time
import udp_protocol
import tcp_protocol
import gobalVariable


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

        gobalVariable.globalV.lock_msg.acquire()
        print( gobalVariable.globalV.lock_msg.locked())
        gobalVariable.globalV.lock_until_end.acquire()
        udpthread = udp_protocol.udp_protocol()
        print('\033[93m' + "udpThred start" + bcolors.ENDC)
        udpthread.start()
        tcpthread = tcp_protocol.tcp_protocol()
        print("tcp thread start")
        tcpthread.start()
        tcpthread.join(10)
        udpthread.join(10)
        print("udp/tcp thread finished")
        # if (len(all_players) != 0):
        # groupsMsg = game1.getGroupsMsg()
        gobalVariable.globalV.lock_msg.release()  # start real_game
        time.sleep(12)
        print("real_game Finished")
        gobalVariable.globalV.lock_until_end.release()
        time.sleep(10)
        gobalVariable.globalV.real_game.goToZero()

        # else:
        #     lock_msg.release()
        #     lock_until_end.release()

    # close all the all_players
    # reset real_game


class ClientThread(threading.Thread):
    groupName = ""
    clientname = ""

    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.clientAddress = clientAddress
        self.csocket = clientsocket

    def run(self):
        print("thread start")
        self.csocket.settimeout(40)  # case no msg recived
        data = self.csocket.recv(2048)
        self.clientname = data.decode()
        self.groupName = gobalVariable.globalV.real_game.addNewGroup(self.clientname)
        while (gobalVariable.globalV.lock_msg.locked()):
            time.sleep(0.01)
        self.startGameMassge()
        # if not val:#player is not playing
        #
        #     return
        while (gobalVariable.globalV.lock_until_end.locked()):
            time.sleep(0.01)
        val = self.sendScore()
        if not val:
            return

    def startGameMassge(self):
        try:
            msg = '\033[95m' + 'Welcome to Keyboard Spamming Battle Royale.\n' + bcolors.ENDC + bcolors.HEADER + bcolors.OKBLUE + bcolors.OKCYAN  + bcolors.ENDC + '\n'
            # self.csocket.send(msg.encode())
            # self.csocket.recv(1024)
            groupsMsg = '\033[94m' + gobalVariable.globalV.real_game.get_group() + bcolors.ENDC
            # self.csocket.send(groupsMsg.encode())
            # self.csocket.recv(1024)
            startMsg = msg + groupsMsg + bcolors.OKGREEN + '\nStart pressing keys on your keyboard as fast as you can!!\n' + bcolors.ENDC
            self.csocket.send(startMsg.encode())

            counter_game = 0
            then = datetime.datetime.now() + datetime.timedelta(seconds=10)
            try:
                while then > datetime.datetime.now():
                    time.sleep(0.01)
                    self.csocket.settimeout(10)
                    if self.csocket.recv(1024):
                        counter_game += 1
            except:
                print("server row 112 --- didnt get typing")
                return False
            print(counter_game)
            print(self.groupName)
            gobalVariable.globalV.real_game.sumScore(counter_game, self.groupName)

        except:
            print("server row 116 ---client lost connection")
            return False

    def sendScore(self):
        try:
            msg = bcolors.WARNING + bcolors.BOLD + gobalVariable.globalV.real_game.calc_total() + bcolors.ENDC
            self.csocket.send(msg.encode())
        except:
            print("server row 126 ---client connection lost")
            return False

if __name__ == '__main__':
    Main()

