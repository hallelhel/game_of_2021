import gobalVariable

class game():
    group1 = []
    group2 = []
    whichGroup = True
    scoreGroup1 = 0
    scoreGroup2 = 0
    winner = ["", 0]
    loser = ["", 0]
    num_of_char = 0

    def goToZero(self):
        self.group1 = []
        self.group2 = []
        self.whichGroup = True
        self.scoreGroup1 = 0
        self.scoreGroup2 = 0
        self.winner = ["", 0]
        self.loser = ["", 0]
        self.num_of_char = 0

    def addNewGroup(self, client_name):
        gobalVariable.globalV.lock_class_game.acquire()
        if self.whichGroup:
            self.group1.append(client_name)
            self.whichGroup = False
            gobalVariable.globalV.lock_class_game.release()
            return "group1"
        else:
            self.group2.append(client_name)
            self.whichGroup = True
            gobalVariable.globalV.lock_class_game.release()
            return "group2"

    def get_group(self):
        message = "group1\n"
        for i in self.group1:
            message += i + "\n"
        message += "group2\n"
        for i in self.group2:
            message += i + "\n"
        return message

    def sumScore(self, counter, group):
        print(counter)
        print(group)
        gobalVariable.globalV.lock_class_game.acquire(True)
        if (group == "group1"):
            self.scoreGroup1 += counter
            print(str(self.scoreGroup1))
        elif ("######"+group == "group2"):
            self.scoreGroup2 += counter
            print("######"+str(self.scoreGroup2))
        self.num_of_char += counter
        gobalVariable.globalV.lock_class_game.relaese()

    def calc_total(self):
        msg = "Game over\ngroup 1 get " + str(self.scoreGroup1) + " points.\n"
        msg += "group 2 get " + str(self.scoreGroup2) + " points.\n"
        msg += "The Winner is:\n"
        if self.scoreGroup1 > self.scoreGroup2:
            msg += str(self.group1)
        elif self.scoreGroup2 > self.scoreGroup1:
            msg += str(self.group2)

        else:
            msg += "Its a teko"
        msg += "\nnice round"
        return msg

