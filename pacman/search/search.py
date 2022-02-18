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
    # mark already visited nodes
    marked = []

    path_queue = util.Stack()
    directions_queue = util.Stack()

    path = [problem.getStartState()]
    directions = []

    path_queue.push(path)
    directions_queue.push(directions)


    while not path_queue.isEmpty():
        path = path_queue.pop()
        directions = directions_queue.pop()

        last_node = path[- 1]

        if (problem.isGoalState(last_node)):
            break

        elif last_node in marked:
            continue

        marked.append(last_node)

        for neighbors in problem.getSuccessors(last_node):

            if not neighbors[0] in path:

                newpath = path.copy()
                newpath.append(neighbors[0])

                new_directions = directions.copy()
                new_directions.append(neighbors[1])

                path_queue.push(newpath)
                directions_queue.push(new_directions)

    return directions

 

def breadthFirstSearch(problem: SearchProblem):

    # mark already visited nodes
    marked = []

    # Priority queue, for paths to be analyzed
    path_queue = util.Queue()
    direction_queue = util.Queue()

    # Append the first node, with "None" as a direction
    path = [problem.getStartState()]
    directions = []

    path_queue.push(path)
    direction_queue.push(directions)


    while not path_queue.isEmpty():
        path = path_queue.pop()
        directions = direction_queue.pop()

        last_node = path[- 1]

        if (problem.isGoalState(last_node)):
            break

        elif last_node in marked:
            continue

        marked.append(last_node)

        for neighbors in problem.getSuccessors(last_node):

            if not neighbors[0] in path:

                newpath = path.copy()
                newpath.append(neighbors[0])

                new_directions = directions.copy()
                new_directions.append(neighbors[1])

                path_queue.push(newpath)
                direction_queue.push(new_directions)

    return directions


def uniformCostSearch(problem: SearchProblem):
    
    frontier = util.PriorityQueue()
    fringe = []
    path = []
    visited = set([])
    priority = 0
    dict = {} 
    start_node = problem.getStartState()

    if problem.isGoalState(start_node):
        return ["Stop"]
    else:
        frontier.push((start_node,path), priority)
        dict[start_node] = 0
        visited.add(start_node)
        while not frontier.isEmpty():
            
            curr, path = frontier.pop()

            if problem.isGoalState(curr):
                return path 
            else:
                
                next = problem.getSuccessors(curr)
                for node in frontier.heap:
                    fringe.append(node[0])
                for states in next:
                    if states[0] not in (key for key in dict):
                        cost=problem.getCostOfActions(path + [states[1]])
                        frontier.push((states[0], path + [states[1]]), cost)
                        dict[states[0]] = cost 
                        visited.add(states[0])


    return path


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
