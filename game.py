import global_variable

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


    def addNewGroup(self, client_name):
        global_variable.globalV.lock_class_game.acquire()
        if self.whichGroup:
            self.group1.append(client_name)
            self.whichGroup = False
            global_variable.globalV.lock_class_game.release()
            return "group1"
        else:
            self.group2.append(client_name)
            self.whichGroup = True
            global_variable.globalV.lock_class_game.release()
            return "group2"

    def get_group(self):
        message = "group1\n"
        for client in self.group1:
            message += client + "\n"
        message += "group2\n"
        for client in self.group2:
            message += client + "\n"
        return message

    def sum_score(self, types, group):
        global_variable.globalV.lock_class_game.acquire()
        if (group == "group1"):
            self.scoreGroup1 += types

        elif (group == "group2"):
            self.scoreGroup2 += types

        global_variable.globalV.lock_class_game.relaese()

    def calc_total(self):
        last_message = "Game over\ngroup 1 get " + str(self.scoreGroup1) + " points.\n"
        last_message += "group 2 get " + str(self.scoreGroup2) + " points.\n"

        if self.scoreGroup1 > self.scoreGroup2:
            last_message += self.group1 + "you win, yours average types was: " + str(self.scoreGroup1/len(self.group1)) + "\n "
            last_message += self.group2 + "nice try, yours average types was: "+ str(self.scoreGroup2/len(self.group2)) + "\n "
        elif self.scoreGroup2 > self.scoreGroup1:
            last_message += self.group2 + "you win the game:\n"
            last_message += self.group1 + "nice try\n"
        else:
            last_message += "we have a tie, think about tiebreaker....\n"
            last_message += "we have a tie, think about tiebreaker....\n"
        last_message += "a little interesting information: the average types for the "
        return last_message

