
POSITION  = 0
DIRECTION = 1
COST      = 2

import queue
import util

    
def depthFirstSearch(problem: SearchProblem):

    visited = set()

    path_stack = util.Stack()

    start_node = problem.getStartState()

    path = []
    path_stack.push((start_node, path))

    if problem.isGoalState(start_node):
        return ["Stop"]
        
    while not path_stack.isEmpty():

        curr_node, path = path_stack.pop()

        if (problem.isGoalState(curr_node)):
            return path

        elif curr_node in visited:
            continue

        visited.add(curr_node)

        neighbors = problem.getSuccessors(curr_node)

        for node in neighbors:

            if not node[POSITION] in visited:

                newpath = path.copy()
                newpath.append(node[DIRECTION])

                path_stack.push((node[POSITION], newpath))

def breadthFirstSearch(problem: SearchProblem):

    visited = set()

    path_stack = util.Queue()

    start_node = problem.getStartState()

    path = []
    path_stack.push((start_node, path))

    if problem.isGoalState(start_node):
        return ["Stop"]

    while not path_stack.isEmpty():

        curr_node, path = path_stack.pop()

        if (problem.isGoalState(curr_node)):
            return path

        elif curr_node in visited:
            continue

        visited.add(curr_node)

        neighbors = problem.getSuccessors(curr_node)

        for node in neighbors:

            if not node[POSITION] in visited:

                newpath = path.copy()
                newpath.append(node[DIRECTION])

                path_stack.push((node[POSITION], newpath))

def uniformCostSearch(problem: SearchProblem):
    
    priority_queue    = util.PriorityQueue()
    path              = []

    visited = set() 

    start_node = problem.getStartState()

    if problem.isGoalState(start_node):
        return ["Stop"]
        
    priority_queue.push((start_node,path), 0)

    while not priority_queue.isEmpty():
        
        # Aqui, o elemento com menor custo sera priorizado
        curr_node, path = priority_queue.pop()

        if problem.isGoalState(curr_node):
            return path 

        neighbors = problem.getSuccessors(curr_node)

        for node in neighbors:

            if node[POSITION] not in visited:

                cost=problem.getCostOfActions(path + [node[DIRECTION]])
                priority_queue.push((node[POSITION], path + [node[DIRECTION]]), cost)

                visited.add(node[POSITION]); 


def nullHeuristic(state, problem=None):
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):

    priority_queue    = util.PriorityQueue()
    path              = []

    visited = set()

    start_node = problem.getStartState()

    if problem.isGoalState(start_node):
        return ["Stop"]

    priority_queue.push((start_node,path), 0)

    while not priority_queue.isEmpty():
        
        # Aqui, o elemento com menor custo sera priorizado
        curr_node, path = priority_queue.pop()

        if problem.isGoalState(curr_node):
            return path

        neighbors = problem.getSuccessors(curr_node)

        for node in neighbors:

            if node[POSITION] not in visited:

                cost=problem.getCostOfActions(path + [node[DIRECTION]]) + heuristic(node[POSITION],problem)
                
                priority_queue.push((node[POSITION], path + [node[DIRECTION]]), cost)
                visited.add(node[POSITION])

bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
