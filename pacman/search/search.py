# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

POSITION  = 0
DIRECTION = 1
COST      = 2

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import queue
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]    
    
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
    path_to_node_cost = {} 

    start_node = problem.getStartState()

    if problem.isGoalState(start_node):
        return ["Stop"]
        
    priority_queue.push((start_node,path), 0)
    path_to_node_cost[start_node] = 0

    while not priority_queue.isEmpty():
        
        curr_node, path = priority_queue.pop()

        if problem.isGoalState(curr_node):
            return path 

        neighbors = problem.getSuccessors(curr_node)

        for node in neighbors:

            if node[POSITION] not in path_to_node_cost:

                cost=problem.getCostOfActions(path + [node[DIRECTION]])
                priority_queue.push((node[POSITION], path + [node[DIRECTION]]), cost)
                path_to_node_cost[node[POSITION]] = cost 


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):

    priority_queue    = util.PriorityQueue()
    path              = []
    path_to_node_cost = {} 

    start_node = problem.getStartState()

    if problem.isGoalState(start_node):
        return ["Stop"]

    priority_queue.push((start_node,path), 0)
    path_to_node_cost[start_node] = 0

    while not priority_queue.isEmpty():
        
        curr_node, path = priority_queue.pop()

        if problem.isGoalState(curr_node):
            return path 

        neighbors = problem.getSuccessors(curr_node)

        for node in neighbors:

            if node[POSITION] not in path_to_node_cost:

                cost=problem.getCostOfActions(path + [node[DIRECTION]]) + heuristic(node[POSITION],problem)
                priority_queue.push((node[POSITION], path + [node[DIRECTION]]), cost)
                path_to_node_cost[node[POSITION]] = cost 


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
