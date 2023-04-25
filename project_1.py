#Student IDs:
#Ailan Hernandez: 
#Melissa Hidalgo: 862211556
#Lucyann Lacdan: 
#Malina Martinez: 
#
#Operations;
#    move a tile up
#    move a tile down
#    move  a tile right
#    move a tile left
#Goal State:
# -------------
# | 1 | 2 | 3 |
# -------------
# | 4 | 5 | 6 |
# -------------
# | 7 | 8 | 0 |
# -------------

#Node class
class Node:
    def __init__(self, state, parent, operation, depth, cost):
        self.state = state
        self.parent = parent
        self.operator = operation
        self.depth = depth
        self.cost = cost
        self.heuristic=None

#parent class
class Search_Alg:
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    #prints the board
    def print_board(curr_state):
        print( "-------------")
        print( "| %i | %i | %i |" % (curr_state[0], curr_state[1], curr_state[2]))
        print( "-------------")
        print( "| %i | %i | %i |" % (curr_state[3], curr_state[4], curr_state[5]))
        print( "-------------")
        print( "| %i | %i | %i |" % (curr_state[6], curr_state[7], curr_state[8]))
        print( "-------------")

    def move_up(curr_state):
        new_state = curr_state
        index = new_state.index(0)
        #check if the index of the empty space is at the top of the board
        if index not in [0, 1, 2]:
            #get tile above empty space
            temp = new_state[index - 3] 
            #push the empty space up
            new_state[index - 3] = 0
            #move tile above empty space down
            new_state[index] = temp
            return new_state
        else: #if tile is on the top row, return an error
            return None
        
    def move_down(curr_state):
        new_state = curr_state
        index = new_state.index(0)
        if index not in [6, 7, 8]:
            temp = new_state[index + 3]
            new_state[index + 3] = 0
            new_state[index] = temp
            return new_state
        else:
            return None
        
    def move_right(curr_state):
        new_state = curr_state
        index = new_state.index(0)
        if index not in [2, 5, 8]:
            temp = new_state[index + 1]
            new_state[index + 1] = 0
            new_state[index] = temp
            return new_state
        else:
            return None
        
    def move_left(curr_state):
        new_state = curr_state
        index = new_state.index(0)
        if index not in [0, 3, 6]:
            temp = new_state[index - 1]
            new_state[index - 1] = 0
            new_state[index] = temp
            return new_state
        else:
            return None
    
    def make_node(state, parent, operator, depth, cost):
        return Node(state, parent, operator, depth, cost)
    
        
#Uniform Cost Search
class Uniform_Cost(Search_Alg):
    def run(self, start_state):
        fringe = []
        path = []

#A* with Misplaced Tile Heuristic
class A_Star_Misplaced(Search_Alg):
    def run(self, start_state):
        fringe = []
        path = []
    
#A* with Euclidean Distance Heuristic
class A_Star_Euclidean(Search_Alg):
    def run(self, start_state):
        fringe = []
        path = []