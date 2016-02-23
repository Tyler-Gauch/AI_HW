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

import util
import searchAgents

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

def graphSearch(problem, frontier):

    startState = problem.getStartState()
    closed = set()
    
    if problem.isGoalState(startState):                        #if we start on the goal state we are done
        return []
    
    for node in problem.getSuccessors(startState):             #add the first nodes successors to the frontier
        addNode(node, [], 0, frontier)
    
    closed.add(startState)                                      #add the first node to the closed list
    

    while not frontier.isEmpty():                                           #for the rest of the nodes do the following
        node = frontier.pop()                                               #get next node
        path = node[1]                                                      #get path took to current node
        cost = node[2]                                                      #get cost taken to current node
        node = node[0]         
        if isinstance(problem, searchAgents.CornersProblem):
            check = node
        else:
            check = node[0]     

        if problem.isGoalState(check):                                    #if it is the goal state return the path
            path.append(node[1])                                            #add node to path before returning
            return path
        
        if not node[0] in closed:                                           #if we havent visted it
            path.append(node[1])                                            #add to the path
            closed.add(node[0])                                          #add to the closed list
            successors = problem.getSuccessors(check)                     #get successor nodes
            for successor in successors:                    
                if not successor[0] in closed:                              #if not in the closed list
                    addNode(successor, list(path), cost, frontier)          #add to the open list

    return path

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    
    stack = util.Stack()

    return graphSearch(problem, stack)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = util.Queue()

    return graphSearch(problem, queue)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    priorityQueue = util.PriorityQueue()

    return graphSearch(problem, priorityQueue)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    priorityHeuristic = PriorityQueueWithHeuristic(heuristic, problem);

    return graphSearch(problem, priorityHeuristic);

def addNode(node, path, cost, frontier):
    cost += node[2]
    if isinstance(frontier, PriorityQueueWithHeuristic):
        frontier.push([node, path, cost])
    elif isinstance(frontier, util.PriorityQueue):
        frontier.push([node, path, cost], cost)
    else:
        frontier.push([node, path, 0])

class PriorityQueueWithHeuristic(util.PriorityQueue):
    def  __init__(self, heuristic, problem):
        self.heuristic = heuristic
        self.problem = problem
        util.PriorityQueue.__init__(self)

    def push(self, node):
        if isinstance(self.problem, searchAgents.PositionSearchProblem):
            util.PriorityQueue.push(self, node, node[2]+ self.heuristic(node[0][0], self.problem))
        else:
            util.PriorityQueue.push(self, node, node[2]+ self.heuristic(node, self.problem))


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
