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


from unittest import result
from pkg_resources import ResolutionError
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

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
        self.index = 0 # Pacman is always agent index 0
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        value =  self.minimax(0, 0, gameState)
        return value[1]
        # util.raiseNotDefined()

    def minimax(self, agent, currentDepth, gameState):
        if(gameState.isWin() or gameState.isLose() or currentDepth == self.depth):
            return [self.evaluationFunction(gameState),'done']

        if(agent == 0):
            scores = []
            gamestates = []
            actions = []
            for i in gameState.getLegalActions(agent):
                gamestates.append(self.minimax(1, currentDepth, gameState.generateSuccessor(agent, i)))
                actions.append(i)
            for i in gamestates:
                scores.append(i[0])
            maxValue = max(scores)
            maxIndex = scores.index(maxValue)
           
            return[gamestates[maxIndex][0], actions[maxIndex]]
            

        else:
            nextAgent = agent + 1
            if(nextAgent == gameState.getNumAgents()):
                nextAgent = 0
            if(nextAgent == 0):
                currentDepth += 1
            scores = []
            gamestates = []
            actions = []
            for i in gameState.getLegalActions(agent):
                gamestates.append(self.minimax(nextAgent, currentDepth, gameState.generateSuccessor(agent, i)))
                actions.append(i)
            for i in gamestates:
                scores.append(i[0])
            
            minValue = min(scores)
            minIndex = scores.index(minValue)
            return [gamestates[minIndex][0], actions[minIndex]]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        value =  self.minimax(0,0,gameState, -99999999, 99999999)
        return value[1]        
        # util.raiseNotDefined()
        
    def minimax(self, agent, currentDepth, gameState, alpha, beta):
        if(gameState.isWin() or gameState.isLose() or currentDepth == self.depth):
            return [self.evaluationFunction(gameState),'done']

        if(agent == 0):
            gamestates = []
            actions = []
            tempMax = -9999999
            index = 0
            legalActions = gameState.getLegalActions(agent)
            for i in range(len(legalActions)):
                gamestates.append(self.minimax(1, currentDepth, gameState.generateSuccessor(agent, legalActions[i]), alpha, beta))
                actions.append(legalActions[i])

                if(tempMax < gamestates[i][0]):
                    tempMax = gamestates[i][0]
                    index = i

                if(tempMax > beta):
                    return [gamestates[index][0], actions[index]]
                alpha = max(alpha, tempMax)
            
            return [gamestates[index][0],actions[index]]          

        else:
            nextAgent = agent + 1
            if(nextAgent == gameState.getNumAgents()):
                nextAgent = 0
            if(nextAgent == 0):
                currentDepth += 1
            gamestates = []
            actions = []
            tempMin = 999999999
            index = 0
            legalActions = gameState.getLegalActions(agent)
            for i in range(len(legalActions)):
                gamestates.append(self.minimax(nextAgent, currentDepth, gameState.generateSuccessor(agent, legalActions[i]), alpha, beta))
                actions.append(legalActions[i])
                if(tempMin > gamestates[i][0]):
                    tempMin = gamestates[i][0]
                    index = i
                if(tempMin < alpha):
                    return [gamestates[index][0],actions[index]]
                beta = min(beta, tempMin)

            return [gamestates[index][0], actions[index]]
    



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
        "*** YOUR CODE HERE ***"

        def expectiMax(gameState, agent,depth):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return [self.evaluationFunction(gameState),0]
            
            if agent == gameState.getNumAgents()-1:
                depth += 1
                nextAgent = self.index
            else:
                nextAgent = agent + 1
            
            returnList = []
            for action in gameState.getLegalActions(agent):
                nextValue = expectiMax(gameState.generateSuccessor(agent,action),nextAgent,depth)
                if agent != self.index:
                    weightedScore = nextValue[0] * (1.0 / len(gameState.getLegalActions(agent)))
                    if returnList == []:
                        returnList.append(weightedScore)
                        returnList.append(action)
                    else:
                        returnList[0] += weightedScore
                        returnList[1] = action
                    
                else:
                    if returnList == []:
                        returnList = [nextValue[0], action]
                    elif nextValue[0] > returnList[0]:
                        returnList = [nextValue[0], action]
            return returnList
        return expectiMax(gameState,self.index, 0)[1]
        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacmanPos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood().asList()
    numCapsules = len(currentGameState.getCapsules())
    numFood = len(currentGameState.getFood().asList())
    currentScore = currentGameState.getScore()

    whiteGhosts = []
    activeGhosts = []

    minActiveGhostDistance = 99999999999
    minWhiteGhostDistance = 99999999999
    minFoodDistance = 999999999

    # for f in food:
    #     tempDist = util.manhattanDistance(pacmanPos, f)
    #     if(minFoodDistance > tempDist):
    #         minFoodDistance = tempDist

    for ghostState in currentGameState.getGhostStates():
        if(ghostState.scaredTimer > 0):
            whiteGhosts.append(ghostState)
        else:
            activeGhosts.append(ghostState)

    if(len(activeGhosts) > 0):
        for g in activeGhosts:
            tempDist = util.manhattanDistance(pacmanPos, g.getPosition())
            if(minActiveGhostDistance > tempDist):
                minActiveGhostDistance = tempDist

    if(len(whiteGhosts) > 0):
        for g in whiteGhosts:
            tempDist = util.manhattanDistance(pacmanPos, g.getPosition())
            if(minWhiteGhostDistance > tempDist):
                minWhiteGhostDistance = tempDist
    


    score = currentScore + -1*minActiveGhostDistance + -1*minWhiteGhostDistance + -30*numCapsules + -4*numFood

    return score
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
