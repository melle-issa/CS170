#Student IDs:
#Ailan Hernandez: 862267773
#Melissa Hidalgo: 862211556
#Lucyann Lacdan: 862132856
#Malina Martinez: 862311483
#
#Operations:
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
        self.totalCost = cost
        self.heuristic = 0

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
            print("The best move to make with g(n) = ", path[i].depth , " and h(n) = ", path[i].heuristic, " is: ")
            print(path[i].operator)
            self.print_board(path[i].state)
            print("\n")

        print("Total moves: ", len(path))

    def check_queue_size(self, current_size, queue_size):
        if current_size < queue_size:
            return queue_size
        else:
            return current_size

    def make_node(self, state, parent, operator, depth, cost):
        return Node(state, parent, operator, depth, cost)
    
    def expand_node(self, input_node):
        options = []

        node1 = self.move_up(input_node.state)
        if(node1 != None):
            options.append(self.make_node(node1, input_node, "move the blank space up", input_node.depth + 1, 0))
        
        node2 = self.move_down(input_node.state)
        if(node2 != None):
            options.append(self.make_node(node2, input_node, "move the blank space down", input_node.depth + 1, 0))

        node3 = self.move_left(input_node.state)
        if(node3 != None):
            options.append(self.make_node(node3, input_node, "move the blank space left", input_node.depth + 1, 0))
        
        node4 = self.move_right(input_node.state)
        if(node4 != None):
            options.append(self.make_node(node4, input_node, "move the blank space right", input_node.depth + 1, 0))

        return options
            

#Uniform Cost Search
class Uniform_Cost(Search_Alg):
    def run(self, start_state):
        root_node = self.make_node(start_state, None, None, 0, 0)
        queue = []
        queue.append(root_node)
        max_in_queue = 0
        expanded_count = 0

        while queue:
            max_in_queue = self.check_queue_size(max_in_queue, len(queue))
            minPos = 0
            for i in range(len(queue)):
                queue[i].totalCost = queue[i].depth
                if(queue[i].totalCost < queue[minPos].totalCost):
                    minPos = i
            currNode = queue.pop(minPos)
            
            if (currNode.state == self.goal_state):
                return [currNode, max_in_queue, expanded_count]
            else:
                expandedOptions = self.expand_node(currNode)
                expanded_count += 1
                for option in expandedOptions:
                    if(option.state != currNode.state):
                        queue.append(option)
                 
        return None

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
        max_in_queue = 0
        expanded_count = 0
        
        while queue:
            max_in_queue = self.check_queue_size(max_in_queue, len(queue))
            minPos = 0
            for i in range(len(queue)):
                queue[i].totalCost = self.getHeuristic(queue[i]) + queue[i].depth
                queue[i].heuristic = self.getHeuristic(queue[i])
                if(queue[i].totalCost < queue[minPos].totalCost):
                    minPos = i
            currNode = queue.pop(minPos)
          
            
            if (currNode.state == self.goal_state):
                return [currNode, max_in_queue, expanded_count]
            else:
                expandedOptions = self.expand_node(currNode)
                expanded_count += 1
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
        max_in_queue = 0
        expanded_count = 0

        while queue:
            max_in_queue = self.check_queue_size(max_in_queue, len(queue))
            minPos = 0
            for i in range(len(queue)):
                queue[i].totalCost = self.getHeuristic(queue[i]) + queue[i].depth
                queue[i].heuristic = self.getHeuristic(queue[i])
                if(queue[i].totalCost < queue[minPos].totalCost):
                    minPos = i
            currNode = queue.pop(minPos)
          
            
            if (currNode.state == self.goal_state):
                return [currNode, max_in_queue, expanded_count]
            else:
                expandedOptions = self.expand_node(currNode)
                expanded_count += 1
                for option in expandedOptions:
                    if(option.state != currNode.state):
                        queue.append(option)
                 
        return None

print("Welcome to our 8 puzzle solver!")
print("1. Use default puzzle")
print("2. Enter your own puzzle")
inp1 = input("Please select which puzzle you'd like to solve: ")
puzzle = []

if inp1 == "2":
    print("Please use a 0 for the blank space in the puzzle and use spaces in between numbers")
    top = list(map(int, input("Please enter the top row of your puzzle: ").strip().split()))
    middle = list(map(int, input("Please enter the middle row of your puzzle: ").strip().split()))
    bottom = list(map(int, input("Please enter the bottom row of your puzzle: ").strip().split()))
    custom_puzzle_list = top + middle + bottom

    i = 0
    for number in custom_puzzle_list:
        puzzle.append(number)
        i += 1

    print("Here's your puzzle: ")
    print(puzzle[0], puzzle[1], puzzle[2])
    print(puzzle[3], puzzle[4], puzzle[5])
    print(puzzle[6], puzzle[7], puzzle[8])

print("Search algorithms:")
print("1. Uniform Cost Search")
print("2. A* with the Misplaced Tile heuristic")
print("3. A* with the Euclidean distance heuristic")
inp2 = input("Please select an algorithm: ")

if inp2 == "1":
    puzzleU = Uniform_Cost()
    if inp1 == "1":
        solutionU=puzzleU.run(puzzleU.default_puzzle)
        print("\nStart state:")
        puzzleU.print_board(puzzleU.default_puzzle)
    else:
        solutionU=puzzleU.run(puzzle)
        print("\nStart state:")
        puzzleU.print_board(puzzle)
    if solutionU is not None:
        puzzleU.trace(solutionU[0])
        print("Goal!")
        print("To solve this puzzle, the search algorithm expanded a total of ", solutionU[2], " nodes.")
        print("The maximum number of nodes in the queue at a time was ", solutionU[1], ".")
        print("The depth of the goal node was ", solutionU[0].depth, ".")
    else:
        print("No solution found.")

elif inp2 == "2":
    puzzleM = A_Misplaced()
    if inp1 == "1":
        solutionM=puzzleM.run(puzzleM.default_puzzle)
        print("\nStart state:")
        puzzleM.print_board(puzzleM.default_puzzle)
    else:
        solutionM=puzzleM.run(puzzle)
        print("\nStart state:")
        puzzleM.print_board(puzzle)
    if solutionM is not None:
        puzzleM.trace(solutionM[0])
        print("Goal!")
        print("To solve this puzzle, the search algorithm expanded a total of ", solutionM[2], " nodes.")
        print("The maximum number of nodes in the queue at a time was ", solutionM[1], ".")
        print("The depth of the goal node was ", solutionM[0].depth, ".")
    else:
        print("No solution found.")

elif inp2 == "3":
    puzzleE = A_EuclideanDist()
    if inp1 == "1":
        solutionE=puzzleE.run(puzzleE.default_puzzle)
        print("\nStart state:")
        puzzleE.print_board(puzzleE.default_puzzle)
    else:
        solutionE=puzzleE.run(puzzle)
        print("\nStart state:")
        puzzleE.print_board(puzzle)
    if solutionE is not None:
        puzzleE.trace(solutionE[0])
        print("Goal!")
        print("To solve this puzzle, the search algorithm expanded a total of ", solutionE[2], " nodes.")
        print("The maximum number of nodes in the queue at a time was ", solutionE[1], ".")
        print("The depth of the goal node was ", solutionE[0].depth, ".")
    else:
        print("No solution found.")