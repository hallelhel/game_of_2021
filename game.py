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

    '''
        add  clients 
        depending on variable 'which group' if odd --> to group 1 , if even --> to group 2               
    '''
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

    '''
    get group1 - clients & group2 - clients              
    '''
    def get_group(self):
        message = "group1\n"
        for client in self.group1:
            message += client + "\n"
        message += "group2\n"
        for client in self.group2:
            message += client + "\n"
        return message

    '''
        sum score -- lock the game for count types 
    '''
    def sum_score(self, types, group):
        global_variable.globalV.lock_class_game.acquire()
        if (group == "group1"):
            self.scoreGroup1 += types

        elif (group == "group2"):
            self.scoreGroup2 += types

        global_variable.globalV.lock_class_game.release()

    '''
    calc total function -- check which group has more scores and print message about the groups and statics information
    '''

    def calc_total(self):

        last_message = "Game over\ngroup 1 get " + str(self.scoreGroup1) + " points.\n"
        last_message += "group 2 get " + str(self.scoreGroup2) + " points.\n"

        max_cuur_play = 0
        avg_grop1 = self.calc_avg(self.scoreGroup1, len(self.group1)) # already str
        avg_grop2 = self.calc_avg(self.scoreGroup2, len(self.group2)) # already str


        if self.scoreGroup1 > self.scoreGroup2:
            last_message += "group1 you win, yours average types per client was: " + str(avg_grop1) + ".\n"
            last_message += "group2  nice try, yours average types per client was: " + str(avg_grop2) + ".\n"
            max_cuur_play = avg_grop1

        elif self.scoreGroup2 > self.scoreGroup1:
            last_message += "group2 you win the game, yours average types per client was: "+ str(avg_grop2) + "\n"
            last_message += "group1 nice try, yours average types per client was: " + str(avg_grop1) + "\n"
            max_cuur_play = avg_grop2

        else:
            last_message += "we have a tie, think about tiebreaker....\n"
            last_message += "yours average types per client was: " + str(avg_grop1) + "\n"
            max_cuur_play = avg_grop1

        last_message += "a little interesting information: the average types for the\n"
        last_message += "max types per client until this game:" + str(global_variable.globalV.max_types_per_player) + "\n"

        if max_cuur_play > global_variable.globalV.max_types_per_player:
            global_variable.globalV.max_types_per_player = max_cuur_play
            last_message += "and you brake the edge\n"

        return last_message

    def calc_avg(self, score_group, group_size):
        if group_size != 0:
            return score_group/group_size
        else:
            return 0

