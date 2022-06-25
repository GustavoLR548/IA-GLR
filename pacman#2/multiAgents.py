PACMAN = 0

class ReflexAgent(Agent):

    def getAction(self, gameState: GameState):

        legalMoves = gameState.getLegalActions()

        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosen_index = random.choice(bestIndices) 

        return legalMoves[chosen_index]

    def evaluationFunction(self, currentGameState: GameState, action):

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

                if min_ghost_distance <= 1 and nearestGhostScaredTime == 0:
                    return [min_ghost_distance, float('-inf')]

                elif min_ghost_distance <= 1 and nearestGhostScaredTime > 0:
                    return [min_ghost_distance, float('inf') ]

            return [min_ghost_distance, nearestGhostScaredTime]

        min_food_distance                        = distance_to_nearest_food(newPos, newFood)
        min_ghost_distance, nearest_scared_ghost = distance_to_nearest_ghost(newPos, successorGameState, newScaredTimes)

        if nearest_scared_ghost == float('inf') or nearest_scared_ghost == float('-inf'):
            return nearest_scared_ghost

        value = successorGameState.getScore() - min_food_distance
        if nearest_scared_ghost > 0:

            value -= min_ghost_distance
        else:
            value += min_ghost_distance

        return value

def scoreEvaluationFunction(currentGameState: GameState):

    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):

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

    def getAction(self, gameState):

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

        possible_actions = self.getLegalActionsWithoutStop(0, gameState)
        alpha = float('-inf')
        beta  = float('inf')

        action_scores = [alphabeta(0, 0, gameState.generateSuccessor(0, action), alpha, beta) for action
                         in possible_actions]

        max_action = max(action_scores)
        max_indices = [index for index in range(len(action_scores)) if action_scores[index] == max_action]
        chosen_index = random.choice(max_indices)

        return possible_actions[chosen_index]

better = betterEvaluationFunction