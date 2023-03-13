# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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

import random
import mdp, util 
from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        #set v(s) for all states s to 0
        for state in self.mdp.getStates():
            self.values[state] = 0 

        for iteration in range(self.iterations): #iterating over
            tempStateValues = util.Counter()
            for state in self.mdp.getStates():
                max = float("-inf")
                actions = self.mdp.getPossibleActions(state)
                if not actions:
                    tempStateValues[state] =0 
                for action in actions:
                    qvalue = self.computeQValueFromValues(state,action)
                    if qvalue > max:
                        max = qvalue
                        tempStateValues[state]=qvalue #updating q value
            self.values = tempStateValues #updating tempvalues into self.values for each iteration at the end
           
                    # print("action",action)
                    # print(self.mdp.getTransitionStatesAndProbs(state, action))
                    # print(self.mdp.getReward(state, action, nextState))
                    # print(self.mdp.isTerminal(state))


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        qvalue=0
        for nextState,probability in self.mdp.getTransitionStatesAndProbs(state,action):
            reward = self.mdp.getReward(state, action, nextState)
            nextStateValue = self.getValue(nextState)
            qvalue += probability*(reward + self.discount*nextStateValue) #Q(s,a) equation
        return qvalue
        # print("action",action)
        # print(self.mdp.getTransitionStatesAndProbs(state, action))
        # #print(self.mdp.getReward(state, action, nextState))
        # print(self.mdp.isTerminal(state))

        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        bestAction = None
        if self.mdp.isTerminal(state): #if terminal state
            return bestAction
        actions = self.mdp.getPossibleActions(state)
        max = float("-inf")
        for action in actions:
            qvalue = self.computeQValueFromValues(state,action)
            if qvalue > max: #getting maximum q value
                max = qvalue
                bestAction = action
            if qvalue == max: # if tie
                bestAction = random.choice([bestAction,action])
        
        return bestAction
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)
    
    

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        for state in self.mdp.getStates():
            self.values[state] = 0
        for iteration in range(self.iterations):
            state  = states[iteration % len(states)] #changing iteration over each state 
            max = float("-inf")
            actions = self.mdp.getPossibleActions(state)
            if not self.mdp.isTerminal(state):
                for action in actions: 
                        qvalue = self.computeQValueFromValues(state,action)
                        if qvalue > max: #getting maximum q value
                            max = qvalue
                self.values[state]=max #update value for each state


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        self.queue = util.PriorityQueue()
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        predecessor = util.Counter()
        
        #followed the given pseudocode in question
        #computing predecessor of states
        for state in self.mdp.getStates():
            predecessor[state] = set()
        for state in self.mdp.getStates():
            actions = self.mdp.getPossibleActions(state)
            for action in actions:
                for nextState,probability in self.mdp.getTransitionStatesAndProbs(state,action):
                    if probability !=0:
                        predecessor[nextState].add(state)
        
        print(predecessor)

       
        for state in self.mdp.getStates():
            max = float("-inf")
            if not self.mdp.isTerminal(state):
                actions = self.mdp.getPossibleActions(state)
                for action in actions:
                    qvalue = self.computeQValueFromValues(state,action)
                    if qvalue > max:
                        max = qvalue
                diff = abs(self.values[state]-max)
                self.queue.update(state,-diff)

        for iteration in range(self.iterations):
            if self.queue.isEmpty():
                return
            state = self.queue.pop()
            if not self.mdp.isTerminal(state):
                actions = self.mdp.getPossibleActions(state)
                max = float("-inf")
                for action in actions:
                    qvalue = self.computeQValueFromValues(state,action)
                    if qvalue > max:
                        max = qvalue
                self.values[state] = max

                
            pds = predecessor[state]
           
            for p in pds:
                if not self.mdp.isTerminal(state):
                    currentVal = self.values[p]
                    max = float("-inf")
                    actions = self.mdp.getPossibleActions(p)
                    for action in actions:
                        qvalue = self.computeQValueFromValues(p,action)
                        if qvalue > max:
                            max = qvalue
                    diff = abs(currentVal-max)
                    if diff > self.theta:
                        self.queue.update(p,-diff)



            
        

