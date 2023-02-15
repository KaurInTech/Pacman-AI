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
import heapq
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

def depthFirstSearch(problem):
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST
    start = problem.getStartState()
    path = []
    depthStack = util.Stack()
    depthStack.push((start,path))
    visitedNode = []
    
    while not depthStack.isEmpty():
        currentState,path = depthStack.pop()
        if currentState in visitedNode:
                continue
        visitedNode.append(currentState)
        if problem.isGoalState(currentState):
            return path
        for neighbour in problem.getSuccessors(currentState):
            depthStack.push((neighbour[0],path+[neighbour[1]]))
      

    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST

    breadthQueue = util.Queue()
    start = problem.getStartState()
    breadthQueue.push((start,[]))
    visitedNode = [start]
    
    while not breadthQueue.isEmpty():
        currentState,path = breadthQueue.pop()
        if problem.isGoalState(currentState):
            return path
        for neighbour in problem.getSuccessors(currentState):
                if neighbour[0] in visitedNode:
                     continue
                breadthQueue.push((neighbour[0],path+[neighbour[1]]))
                visitedNode.append(neighbour[0])

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST
    "*** YOUR CODE HERE ***"

    uniformQueue = util.PriorityQueue()
    start = problem.getStartState()
    visitedNode = []
    uniformQueue.push( (start, []), 0 )

    while not uniformQueue.isEmpty():
        currentState,path = uniformQueue.pop()
        if currentState in visitedNode:
                continue
        visitedNode.append(currentState)
        if problem.isGoalState(currentState):
            return path
        for neighbour in problem.getSuccessors(currentState):
                uniformQueue.update( (neighbour[0], path + [neighbour[1]]), problem.getCostOfActions(path+[neighbour[1]]) )
      
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    astarQueue = util.PriorityQueue()
    visitednode = []
    astarQueue.push( (start, []), heuristic(start, problem) )

    while not astarQueue.isEmpty():
        currentState, path = astarQueue.pop()
        if currentState in visitednode:
                continue
        visitednode.append(currentState)
        if problem.isGoalState(currentState):
            return path
        for neighbour in problem.getSuccessors(currentState):
                astarQueue.update(
                (neighbour[0],path+[neighbour[1]]),
                problem.getCostOfActions(path+[neighbour[1]])+heuristic(neighbour[0], problem)
                )
   
    util.raiseNotDefined()
       


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
