# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

PACMAN = 0

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosen_index = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosen_index]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        def distance_to_nearest_food(newPos, newFood):
            newFoodList       = np.array(newFood.asList())
            distanceToFood    = [util.manhattanDistance(newPos, food) for food in newFoodList]
            min_food_distance = 0
            if len(newFoodList) > 0:
                min_food_distance = distanceToFood[np.argmin(distanceToFood)]

            return min_food_distance

        def distance_to_nearest_ghost(newPos, successorGameState, newScaredTimes):
            ghostPositions = np.array(successorGameState.getGhostPositions())
            distanceToGhosts = [util.manhattanDistance(newPos, ghost) for ghost in ghostPositions]
            min_ghost_distance = 0
            nearestGhostScaredTime = 0

            if len(ghostPositions) > 0:
                min_ghost_distance     = distanceToGhosts[np.argmin(distanceToGhosts)]
                nearestGhostScaredTime = newScaredTimes[np.argmin(distanceToGhosts)]

                # Pacman is near a ghost that isnt scared
                if min_ghost_distance <= 1 and nearestGhostScaredTime == 0:
                    return [min_ghost_distance, float('-inf')]
                # Pacman is near a ghost that is scared
                elif min_ghost_distance <= 1 and nearestGhostScaredTime > 0:
                    return [min_ghost_distance, float('inf') ]

            return [min_ghost_distance, nearestGhostScaredTime]

        min_food_distance                        = distance_to_nearest_food(newPos, newFood)
        min_ghost_distance, nearest_scared_ghost = distance_to_nearest_ghost(newPos, successorGameState, newScaredTimes)

        if nearest_scared_ghost == float('inf') or nearest_scared_ghost == float('-inf'):
            return nearest_scared_ghost

        value = successorGameState.getScore() - min_food_distance
        if nearest_scared_ghost > 0:
            # Follow ghosts that are scared
            value -= min_ghost_distance
        else:
            value += min_ghost_distance

        return value

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def getLegalActionsWithoutStop(self, index, gameState):

        illegal_action = Directions.STOP

        possible_actions = gameState.getLegalActions(index)
        if illegal_action in possible_actions:
            possible_actions.remove(illegal_action)

        return possible_actions

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):

        def minimax(agent, depth, gameState):

            def minimize(agent,depth, gameState):
                nextAgent = agent + 1
                if gameState.getNumAgents() == nextAgent:
                    nextAgent = PACMAN 

                if nextAgent == PACMAN: 
                    depth += 1

                return min(minimax(nextAgent, depth, gameState.generateSuccessor(agent, action)) for action in
                        self.getLegalActionsWithoutStop(agent, gameState))

            def maximize(agent,depth, gameState):
                return max(minimax(1, depth, gameState.generateSuccessor(agent, action)) for action in
                    self.getLegalActionsWithoutStop(0, gameState))

            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState)

            if agent == PACMAN:  
                return maximize(agent, depth, gameState)

            else:  
                return minimize(agent, depth, gameState)

        # Code starts here #
        possible_actions = self.getLegalActionsWithoutStop(0, gameState)
        action_scores   = [minimax(0, 0, gameState.generateSuccessor(0, action)) for action
                         in possible_actions]

        max_action  = max(action_scores)
        max_indices = [index for index in range(len(action_scores)) if action_scores[index] == max_action]
        chosen_index = random.choice(max_indices)

        return possible_actions[chosen_index]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction using alpha-beta pruning.
        """
        def alphabeta(agent, depth, gameState, alpha, beta):

            def minimize(agent, depth, gameState, alpha, beta):
                value = float('-inf')
                for action in self.getLegalActionsWithoutStop(agent, gameState):
                    value = max(value, alphabeta(1, depth, gameState.generateSuccessor(agent, action), alpha, beta))
                    alpha = max(alpha, value)
                    
                    if beta <= alpha: 
                        break
                return value

            def maximize(agent,depth, gameState, alpha, beta):
                nextAgent = agent + 1 
                if gameState.getNumAgents() == nextAgent:
                    nextAgent = PACMAN 

                if nextAgent == PACMAN: 
                    depth += 1

                for action in self.getLegalActionsWithoutStop(agent, gameState):
                    value = float('inf')

                    value = min(value, alphabeta(nextAgent, depth, gameState.generateSuccessor(agent, action), alpha, beta))
                    beta  = min(beta, value)

                    if beta <= alpha: 
                        break

                return value

            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState)

            if agent == PACMAN: 
                return minimize(agent,depth,gameState,alpha,beta)
            else: 
                return maximize(agent,depth,gameState,alpha,beta)

        # Code starts here #
        possible_actions = self.getLegalActionsWithoutStop(0, gameState)
        alpha = float('-inf')
        beta  = float('inf')

        action_scores = [alphabeta(0, 0, gameState.generateSuccessor(0, action), alpha, beta) for action
                         in possible_actions]

        max_action = max(action_scores)
        max_indices = [index for index in range(len(action_scores)) if action_scores[index] == max_action]
        chosen_index = random.choice(max_indices)

        return possible_actions[chosen_index]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction