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
    default_puzzle = [2, 3, 5, 4, 1, 8, 6, 0, 7]

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
    
    def expand(self, input_node):
        options = []

        node1 = self.move_up(input_node.state)
        if(node1 != None):
            options.append(self.make_node(node1, input_node, "move blank space up", input_node.depth + 1, 0))
        
        node2 = self.move_down(input_node.state)
        if(node2 != None):
            options.append(self.make_node(node2, input_node, "move blank space down", input_node.depth + 1, 0))

        node3 = self.move_left(input_node)
        if(node3 != None):
            options.append(self.make_node(node3, input_node, "move blank space left", input_node.depth + 1, 0))
        
        node4 = self.move_right(input_node)
        if(node4 != None):
            options.append(self.make_node(node4, input_node, "move blank space right", input_node.depth + 1, 0))
            

#Uniform Cost Search
class Uniform_Cost(Search_Alg):
    def ascending_sort(frontier):
        frontier.sort(key =lambda x: x.depth)

    def run(self, start_state):
        root_node = self.make_node(start_state, None, None, 0, 0)
        fringe = []
        fringe.append(root_node)
        explored = []
        path = []
        while True:
            #if empty and no solution return failure
            if fringe == [] : return []
            #pick node with lowest cost of action
            fringe = self.ascending_sort(fringe)
            current_node = fringe.pop(0)
            #add that operation to the path
            path.append(current_node.operator)
            #if it's the goal state, return a success
            if current_node.state == self.goal_state : return path
            #otherwise, explore your options at that node
            explored.append(current_node)
            expanded_nodes = self.expand(current_node)
            #add its children to the frontier
            for node in expanded_nodes:
                index = explored.index(current_node)
                #if we haven't seen this child yet, add to fringe
                if(index < 0): fringe.append(node)
                #otherwise, see if we've seen this child but at a higher cost
                elif fringe[index].depth < node.depth : 
                    fringe.pop(index)
                    fringe.append(node)



#A* with Misplaced Tile Heuristic
# class A_Star_Misplaced(Search_Alg):
#     def run(self, start_state):
#         fringe = []
#         path = []
    
# #A* with Euclidean Distance Heuristic
# class A_Star_Euclidean(Search_Alg):
#     def run(self, start_state):
#         fringe = []
#         path = []