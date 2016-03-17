from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

# Tyler Gauch
# COMP 3770 01
# 3/17/2016

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
            if alpha < tempValue:
                alpha = tempValue
                bestAction = action

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
            tempValue = self.expValue(gameState.generateSuccessor(0, action), 1, 1)
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
        if len(gameState.getLegalActions(agentIndex)) == 0:
            return self.evaluationFunction(gameState)
        for action in gameState.getLegalActions(agentIndex):
            bestValue += self.probability(gameState, agentIndex) * self.value(gameState.generateSuccessor(agentIndex, action), agentIndex, currentDepth)

        return bestValue

    def probability(self, gameState, agentIndex):
        return 1.0 / (len(gameState.getLegalActions(agentIndex)) * 1.0)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: First thing we do is check if we won or lost.  We do not make these return infinity incase 
                    we have more than one action that returns a terminal node the average will be higher for 
                    a terminal node that took 1 step vs 2 steps.  Next we calculate the distance to the ghosts 
                    and subtract the distance from the ghost.  This keeps us close enough to the ghost to keep
                    moving but far enough away to never die.  Lastly we subtract the distance to the closest food.
                    This says that the closer we are to the food the better.
    """
    pos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood()

    score = currentGameState.getScore()

    if currentGameState.isWin():
        score = 100000
    if currentGameState.isLose():
        score = -100000

    distanceThreshold = 3

    for i in range(currentGameState.getNumAgents()):
        if i == 0:
            continue
        ghostDistance = max(util.manhattanDistance(pos, currentGameState.getGhostPosition(i)), distanceThreshold)
        score -= ghostDistance 

    currentFood = currentFood.asList()

    closestFood = 100
    for food in currentFood:
        distance = util.manhattanDistance(food, pos)
        closestFood = min(closestFood, distance)

    score -= closestFood

    return score


better = betterEvaluationFunction