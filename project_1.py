#Student IDs:
#Ailan Hernandez: 86
#Melissa Hidalgo: 862211556
#Lucyann Lacdan: 862132856
#Malina Martinez: 
#
#Operations;
#    move a tile up
#    move a tile down
#    move  a tile right
#    move a tile left
#Goal State:
# 1 2 3
# 4 5 6
# 7 8 0

#Node class
from math import sqrt

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
    default_puzzle = [1, 5, 0, 8, 3, 6, 4, 2, 7]

    def __init__(self) -> None:
        pass

    #prints the board
    def print_board(self, curr_state):
        print(curr_state[0], curr_state[1], curr_state[2])
        print(curr_state[3], curr_state[4], curr_state[5])
        print(curr_state[6], curr_state[7], curr_state[8])

    def move_up(self, curr_state):
        new_state = curr_state.copy()
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
        
    def move_down(self, curr_state):
        new_state = curr_state.copy()
        index = new_state.index(0)
        if index not in [6, 7, 8]:
            temp = new_state[index + 3]
            new_state[index + 3] = 0
            new_state[index] = temp
            return new_state
        else:
            return None
        
    def move_right(self, curr_state):
        new_state = curr_state.copy()
        index = new_state.index(0)
        if index not in [2, 5, 8]:
            temp = new_state[index + 1]
            new_state[index + 1] = 0
            new_state[index] = temp
            return new_state
        else:
            return None
        
    def move_left(self, curr_state):
        new_state = curr_state.copy()
        index = new_state.index(0)
        if index not in [0, 3, 6]:
            temp = new_state[index - 1]
            new_state[index - 1] = 0
            new_state[index] = temp
            return new_state
        else:
            return None
        
    def trace(self, node):
        path = []

        while node.parent != None:
            #path.append(node.operator)
            path.append(node)
            #self.print_board(node.state)
            node = node.parent
        path.reverse()

        for i in range(len(path)):
            print(path[i].operator)
            self.print_board(path[i].state)

        print("Total moves: ", len(path))

    
    def make_node(self, state, parent, operator, depth, cost):
        return Node(state, parent, operator, depth, cost)
    
    def expand_node(self, input_node):
        options = []

        node1 = self.move_up(input_node.state)
        if(node1 != None):
            options.append(self.make_node(node1, input_node, "move blank space up", input_node.depth + 1, 0))
        
        node2 = self.move_down(input_node.state)
        if(node2 != None):
            options.append(self.make_node(node2, input_node, "move blank space down", input_node.depth + 1, 0))

        node3 = self.move_left(input_node.state)
        if(node3 != None):
            options.append(self.make_node(node3, input_node, "move blank space left", input_node.depth + 1, 0))
        
        node4 = self.move_right(input_node.state)
        if(node4 != None):
            options.append(self.make_node(node4, input_node, "move blank space right", input_node.depth + 1, 0))

        return options
            

#Uniform Cost Search
class Uniform_Cost(Search_Alg):
    #sorts the nodes in the frontier by their depth
    def ascending_sort(self, frontier):
        new_frontier = frontier.sort(key =lambda x: x.depth)
        return new_frontier

    def check_queue_size(self, current_size, queue_size):
        if current_size < queue_size:
            return queue_size
        else:
            return current_size

    def run(self, start_state):
        root_node = self.make_node(start_state, None, None, 0, 0)
        fringe = []
        fringe.append(root_node)
        explored = []
        expanded_count = 0
        max_in_queue = 0
        while True:
            #if empty and no solution return failure
            if not fringe: return None
            #pick node with lowest cost of action
            fringe = self.ascending_sort(fringe)
            max_in_queue = self.check_queue_size(max_in_queue, len(fringe))
            current_node = fringe.pop(0)
            #if it's the goal state, return a success
            if current_node.state == self.goal_state : return [current_node, expanded_count, max_in_queue]
            #otherwise, explore your options at that node
            explored.append(current_node)
            expanded_nodes = self.expand_node(current_node)
            expanded_count += 1
            #add its children to the frontier
            for node in expanded_nodes:
                #if we haven't seen this child yet, add to fringe
                if node not in expanded_nodes:
                    fringe.append(node)
                #otherwise, see if we've seen this child but at a higher cost
                elif fringe.index(node).depth < node.depth :
                    #replace node with it's lower cost route
                    fringe[fringe.index(node)] = node


#A* Misplaced Tile Heuristic 
class A_Misplaced(Search_Alg):
    def getHeuristic(self, node):
        heuristic = 0
        for i in range(len(node.state)):
            if node.state[i] != Search_Alg.goal_state[i]:
                heuristic += 1
        return heuristic

    def run(self, start_state):
        root_node = self.make_node(start_state, None, None, 0, 0)
        queue = []
        queue.append(root_node)
        
        
        while queue:
            minPos = 0
            for i in range(len(queue)):
                queue[i].totalCost = self.getHeuristic(queue[i]) + queue[i].depth
                if(queue[i].totalCost < queue[minPos].totalCost):
                    minPos = i
            currNode = queue.pop(minPos)
          
            
            if (currNode.state == self.goal_state):
                return currNode
            else:
                expandedOptions = self.expand_node(currNode)
                for option in expandedOptions:
         
                    if(option.state != currNode.state):
                        queue.append(option)
             
                        
        return None

# A* with Euclidean Distance Heuristic
class A_EuclideanDist(Search_Alg):
    def getHeuristic(self, node):
        heuristic = 0
        for i in range(len(node.state)):
            #distance formula
            if node.state[i] != 0:
                distance = sqrt((node.state[i] % 3 - Search_Alg.goal_state[i] % 3)**2 + (node.state[i] // 3 - Search_Alg.goal_state[i] // 3)**2)
                heuristic += distance
        return heuristic
    
    def run(self, start_state):
        root_node = self.make_node(start_state, None, None, 0, 0)
        queue = []
        queue.append(root_node)

        while queue:
            minPos = 0
            for i in range(len(queue)):
                queue[i].totalCost = self.getHeuristic(queue[i]) + queue[i].depth
                if(queue[i].totalCost < queue[minPos].totalCost):
                    minPos = i
            currNode = queue.pop(minPos)
          
            
            if (currNode.state == self.goal_state):
                return currNode
            else:
                expandedOptions = self.expand_node(currNode)
                for option in expandedOptions:
                    if(option.state != currNode.state):
                        queue.append(option)
                 
        return None

# puzzleM = A_Misplaced()
# puzzleM.print_board(puzzleM.default_puzzle)
# solutionM=puzzleM.run(puzzleM.default_puzzle)
# if solutionM is not None:
#     puzzleM.trace(solutionM)
# else:
#     print("No solution found.")


puzzleE = A_EuclideanDist()
puzzleE.print_board(puzzleE.default_puzzle)
solutionE=puzzleE.run(puzzleE.default_puzzle)
if solutionE is not None:
    puzzleE.trace(solutionE)
else:
    print("No solution found")

#puzzle = Uniform_Cost()
#solution = puzzle.run(puzzle.default_puzzle)
#if solution != None:
    #print("Nodes expanded: ", solution[1])
    #print("Max in queue: ", solution[2])

#A* with Misplaced Tile Heuristic



# class A_Star_Misplaced(Search_Alg):
#     def run(self, start_state):
#         fringe = []
    
# #A* with Euclidean Distance Heuristic
# class A_Star_Euclidean(Search_Alg):
#     def run(self, start_state):
#         fringe = []