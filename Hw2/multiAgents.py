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

# Tyler Gauch
# COMP 3770 01
# 1/28/2015


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
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

        """
        STEPS:
            1) Check if we will win if so do this.
            2) Check if we will lose if so dont do this
            3) Dont hit a ghost
                a) Compute distances to ghosts
                b) Only do if we haven't eaten a capsul 
                c) if ghost is too close dont do this
            4) Check where the food is
                a) Find food x,y
                b) Find distance to nearest food pellet
                c) remove the distance from the score
            EDIT: Never stop its just a waste of time
            EDIT: Add check to see if food exists in currentGameState at a position we moved to
                    so we dont just float around the food
        """


        if successorGameState.isWin():  #check if win
            return 200000
        elif successorGameState.isLose():   #check if lose
            return -200000
        elif action == 'Stop':  #dont stop
           return -20000

        score = successorGameState.getScore() #start with new score we will get

        #init some variables
        ghostEval = 0              #eval for ghosts
        distanceThreshold = 2       #how far to stay away from the ghosts
        timeThreshold = 1           #how long to wait until we care bout ghosts again



        for i in range(len(newGhostStates)):
            #check if we even care about the ghosts because we ate a capsule and it 
            #is within the time threashold
            if len(newScaredTimes) > i and newScaredTimes[i] < timeThreshold:
            		#get the distance to the ghost
                    ghostDistance = util.manhattanDistance(newPos, newGhostStates[i].getPosition())
                    #if it is too close dont do this
                    if ghostDistance < distanceThreshold:
                        newEval = -10000 + ghostDistance;
                        if ghostEval > newEval:
                            ghostEval = newEval # keep hold of closest ghost


        if ghostEval < 0:
            return ghostEval # return if we don't want to do this

        newFood = newFood.asList() #get list of trues and their x and y

        if currentGameState.hasFood(newPos[0], newPos[1]): #if the next tile has food thats the closest food
            score += 100
        else:
        	#find closest food
            closestFood = 100
            for food in newFood:
                distance = util.manhattanDistance(food, newPos)
                if distance < closestFood:
                    closestFood = distance
            score -= closestFood #subtract the distance therefore closeset food has better score

        #return the score for this move
        return score

