# 2016.03.15 11:34:28 EDT
#Embedded file name: multiAgents.py
from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

def scoreEvaluationFunction(currentGameState):
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
        self.index = 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        bestValue = float('-Inf')
        bestAction = None
        for action in gameState.getLegalActions(0):
            tempValue = self.minValue(gameState.generateSuccessor(0, action), 1, 1)
            print action, ' - ', tempValue
            if bestValue < tempValue:
                bestValue = tempValue
                bestAction = action

        return bestAction

    def value(self, gameState, agentIndex, currentDepth):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        elif agentIndex == gameState.getNumAgents() - 1:
            return self.maxValue(gameState, 0, currentDepth)
        else:
            return self.minValue(gameState, agentIndex + 1, currentDepth)

    def maxValue(self, gameState, agentIndex, currentDepth):
        currentDepth += 1
        if currentDepth > self.depth:
            return self.evaluationFunction(gameState)
        bestValue = float('-Inf')
        for action in gameState.getLegalActions(agentIndex):
            bestValue = max(bestValue, self.value(gameState.generateSuccessor(agentIndex, action), agentIndex, currentDepth))

        return bestValue

    def minValue(self, gameState, agentIndex, currentDepth):
        bestValue = float('Inf')
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState)
        for action in gameState.getLegalActions(agentIndex):
            bestValue = min(bestValue, self.value(gameState.generateSuccessor(agentIndex, action), agentIndex, currentDepth))

        return bestValue


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        bestAction = None
        alpha = float('-Inf')
        beta = float('Inf')
        for action in gameState.getLegalActions(0):
            tempValue = self.minValue(gameState.generateSuccessor(0, action), 1, 1, alpha, beta)
            print action, ' - ', tempValue
            if alpha < tempValue:
                alpha = tempValue
                bestAction = action

        print bestAction, ' ', alpha, '\n ', gameState
        return bestAction

    def value(self, gameState, agentIndex, currentDepth, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        elif agentIndex == gameState.getNumAgents() - 1:
            return self.maxValue(gameState, 0, currentDepth, alpha, beta)
        else:
            return self.minValue(gameState, agentIndex + 1, currentDepth, alpha, beta)

    def maxValue(self, gameState, agentIndex, currentDepth, alpha, beta):
        currentDepth += 1
        if currentDepth > self.depth:
            return self.evaluationFunction(gameState)
        bestValue = float('-Inf')
        for action in gameState.getLegalActions(agentIndex):
            bestValue = max(bestValue, self.value(gameState.generateSuccessor(agentIndex, action), agentIndex, currentDepth, alpha, beta))
            if bestValue > beta:
                return bestValue
            alpha = max(alpha, bestValue)

        return bestValue

    def minValue(self, gameState, agentIndex, currentDepth, alpha, beta):
        bestValue = float('Inf')
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState)
        for action in gameState.getLegalActions(agentIndex):
            bestValue = min(bestValue, self.value(gameState.generateSuccessor(agentIndex, action), agentIndex, currentDepth, alpha, beta))
            if bestValue < alpha:
                return bestValue
            beta = min(beta, bestValue)

        return bestValue


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        bestValue = float('-Inf')
        bestAction = None
        for action in gameState.getLegalActions(0):
            print 'Checking action: ', action
            tempValue = self.expValue(gameState.generateSuccessor(0, action), 1, 1)
            print action, ' - ', tempValue
            if bestValue < tempValue:
                bestValue = tempValue
                bestAction = action

        print bestAction, ' ', bestValue, '\n ', gameState
        return bestAction

    def value(self, gameState, agentIndex, currentDepth):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        elif agentIndex == gameState.getNumAgents() - 1:
            return self.maxValue(gameState, 0, currentDepth)
        else:
            return self.expValue(gameState, agentIndex + 1, currentDepth)

    def maxValue(self, gameState, agentIndex, currentDepth):
        currentDepth += 1
        if currentDepth > self.depth:
            return self.evaluationFunction(gameState)
        bestValue = float('-Inf')
        for action in gameState.getLegalActions(agentIndex):
            bestValue = max(bestValue, self.value(gameState.generateSuccessor(agentIndex, action), agentIndex, currentDepth))

        return bestValue

    def expValue(self, gameState, agentIndex, currentDepth):
        bestValue = 0
        for action in gameState.getLegalActions(agentIndex):
            bestValue += self.probability(gameState, agentIndex) * self.value(gameState.generateSuccessor(agentIndex, action), agentIndex, currentDepth)

        return bestValue

    def probability(self, gameState, agentIndex):
        return 1.0 / (len(gameState.getLegalActions(agentIndex)) * 1.0)


class AlphaBetaEvalAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        bestAction = None
        alpha = float('-Inf')
        beta = float('Inf')
        for action in gameState.getLegalActions(0):
            tempValue = self.minValue(gameState.generateSuccessor(0, action), 1, 1, alpha, beta)
            print action, ' - ', tempValue
            if alpha < tempValue:
                alpha = tempValue
                bestAction = action

        print bestAction, ' ', alpha, '\n ', gameState
        return alpha

    def value(self, gameState, agentIndex, currentDepth, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        elif agentIndex == gameState.getNumAgents() - 1:
            return self.maxValue(gameState, 0, currentDepth, alpha, beta)
        else:
            return self.minValue(gameState, agentIndex + 1, currentDepth, alpha, beta)

    def maxValue(self, gameState, agentIndex, currentDepth, alpha, beta):
        currentDepth += 1
        if currentDepth > self.depth:
            return self.evaluationFunction(gameState)
        bestValue = float('-Inf')
        for action in gameState.getLegalActions(agentIndex):
            bestValue = max(bestValue, self.value(gameState.generateSuccessor(agentIndex, action), agentIndex, currentDepth, alpha, beta))
            if bestValue > beta:
                return bestValue
            alpha = max(alpha, bestValue)

        return bestValue

    def minValue(self, gameState, agentIndex, currentDepth, alpha, beta):
        bestValue = float('Inf')
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState)
        for action in gameState.getLegalActions(agentIndex):
            bestValue = min(bestValue, self.value(gameState.generateSuccessor(agentIndex, action), agentIndex, currentDepth, alpha, beta))
            if bestValue < alpha:
                return bestValue
            beta = min(beta, bestValue)

        return bestValue


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      1. Avoid Ghosts
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ ghostState.scaredTimer for ghostState in newGhostStates ]
    if currentGameState.isWin():
        return 200000
    if currentGameState.isLose():
        return -200000
    score = currentGameState.getScore()
    ghostEval = 0
    distanceThreshold = 2
    timeThreshold = 1
    for i in range(len(newGhostStates)):
        if len(newScaredTimes) > i and newScaredTimes[i] < timeThreshold:
            ghostDistance = util.manhattanDistance(newPos, newGhostStates[i].getPosition())
            if ghostDistance < distanceThreshold:
                newEval = -10000 + ghostDistance
                if ghostEval > newEval:
                    ghostEval = newEval

    if ghostEval < 0:
        return ghostEval
    newFood = newFood.asList()
    if currentGameState.hasFood(newPos[0], newPos[1]):
        score += 100
    else:
        closestFood = 100
        for food in newFood:
            distance = util.manhattanDistance(food, newPos)
            if distance < closestFood:
                closestFood = distance

        score -= closestFood
    agent = AlphaBetaEvalAgent('scoreEvaluationFunction', 1)
    score += agent.getAction(currentGameState)
    return score


better = betterEvaluationFunction