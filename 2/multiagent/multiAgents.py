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
        legalMoves = gameState.getlegal_actions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

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
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        if successorGameState.isWin():
            return 1000000
        
        foodList = newFood.asList()
        from util import manhattanDistance
        foodDistance = [0]
        for pos in foodList:
            foodDistance.append( manhattanDistance(newPos,pos) )
            
        ghostPos = []
        for ghost in newGhostStates:
            ghostPos.append(ghost.getPosition())

        ghostDistance = []
        for pos in ghostPos:
            ghostDistance.append(manhattanDistance(newPos,pos))

        ghostPosCurrent = []
        for ghost in currentGameState.getGhostStates():
            ghostPosCurrent.append(ghost.getPosition())

        ghostDistanceCurrent = []
        for pos in ghostPosCurrent:
            ghostDistanceCurrent.append(manhattanDistance(newPos,pos))
            
        score = 0
        numberOfFoodLeft = len(foodList)
        numberOfFoodLeftCurrent = len(currentGameState.getFood().asList())
        numberofPowerPellets = len(successorGameState.getCapsules())
        sumScaredTimes = sum(newScaredTimes)
        
        score += successorGameState.getScore() - currentGameState.getScore()
        if action == Directions.STOP:
            score -= 10
            
        if newPos in currentGameState.getCapsules():
            score += 150 * numberofPowerPellets
        if numberOfFoodLeft < numberOfFoodLeftCurrent:
            score += 200

        score -= 10 * numberOfFoodLeft

        if sumScaredTimes > 0 :
            if min(ghostDistanceCurrent) < min(ghostDistance):
                score += 200
            else:
                score -=100
        else:
            if min(ghostDistanceCurrent) < min(ghostDistance):
                score -= 100
            else:
                score += 200
        
        return score
        

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
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getlegal_actions(agent_index):
        Returns a list of legal actions for an agent
        agent_index=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agent_index, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def min_level(state, agent_index, depth):
            legal_actions = state.getLegalActions(agent_index)
            if not legal_actions: 
                return self.evaluationFunction(state)

            if agent_index == state.getNumAgents() - 1:
                return min(max_level(state.generateSuccessor(agent_index, action), depth) for action in legal_actions)
            else:
                return min(min_level(state.generateSuccessor(agent_index, action), agent_index + 1, depth) for action in
                           legal_actions)

        def max_level(state, depth):
            legal_actions = state.getLegalActions(0)
            if not legal_actions or depth == self.depth:
                return self.evaluationFunction(state)

            return max(min_level(state.generateSuccessor(0, action), 1, depth + 1) for action in legal_actions)

        best_action = max(gameState.getLegalActions(0),
                         key=lambda action: min_level(gameState.generateSuccessor(0, action), 1, 1))
        return best_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def min_level(state, agent_index, depth, alpha, beta):
            legal_actions = state.getLegalActions(agent_index)
            if not legal_actions:
                return self.evaluationFunction(state)

            value = 1000000
            for action in legal_actions:
                new_move = state.generateSuccessor(agent_index, action)

                if agent_index == state.getNumAgents() - 1:
                    new_value = max_level(new_move, depth, alpha, beta)
                else:
                    new_value = min_level(new_move, agent_index + 1, depth, alpha, beta)

                value = min(value, new_value)
                if value < alpha:
                    return value
                beta = min(beta, value)
            return value

        def max_level(state, depth, alpha, beta):
            legal_actions = state.getLegalActions(0)
            if not legal_actions or depth == self.depth:
                return self.evaluationFunction(state)

            value = -1000000
            
            for action in legal_actions:
                new_move = state.generateSuccessor(0, action)
                new_value = min_level(new_move, 1, depth + 1, alpha, beta)
                if new_value > value:
                    value = new_value
                if value > beta:
                    return value
                alpha = max(alpha, value)

            return value

        
        best_action = max(gameState.getLegalActions(0),
                         key=lambda action: min_level(gameState.generateSuccessor(0, action), 1, 1, -1000000, 1000000))
        return best_action

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
        def max_level(state, depth):
            legal_actions = state.getLegalActions(0)
            if not legal_actions or depth == self.depth:
                return self.evaluationFunction(state)

            return max(expected_value(state.generateSuccessor(0, action), 1, depth + 1) for action in legal_actions)
        
        def expected_value(state, agent_index, depth):
            legal_actions = state.getLegalActions(agent_index)
            if not legal_actions:
                return self.evaluationFunction(state)

            value = 0
            for action in legal_actions:
                new_move = state.generateSuccessor(agent_index, action)
                if agent_index == state.getNumAgents() - 1:
                    value += max_level(new_move, depth)
                else:
                    value += expected_value(new_move, agent_index + 1, depth)
            return value / len(legal_actions)

        best_action = max(gameState.getLegalActions(0),
                         key=lambda action: expected_value(gameState.generateSuccessor(0, action), 1, 1))
        return best_action

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
