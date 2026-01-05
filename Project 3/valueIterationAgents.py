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

    def __init__(self, mdp: mdp.MarkovDecisionProcess, discount=0.9, iterations=100):
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
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for _ in range(self.iterations):
            new_values = util.Counter()
            for state in self.mdp.getStates():
                if self.mdp.isTerminal(state):
                    new_values[state] = 0
                else:
                    new_values[state] = max(
                        self.computeQValueFromValues(state, action)
                        for action in self.mdp.getPossibleActions(state)
                    )
            self.values = new_values.copy()

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
        qvalue = 0
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            qvalue += prob * (
                self.mdp.getReward(state, action, nextState)
                + self.discount * self.values[nextState]
            )
        return qvalue
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
        maximum = (-float("inf"), None)
        for action in self.mdp.getPossibleActions(state):
            qvalue = self.computeQValueFromValues(state, action)
            maximum = max(maximum, (qvalue, action))
        return maximum[1]
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class PrioritizedSweepingValueIterationAgent(ValueIterationAgent):
    """
    * Please read learningAgents.py before reading this.*

    A PrioritizedSweepingValueIterationAgent takes a Markov decision process
    (see mdp.py) on initialization and runs prioritized sweeping value iteration
    for a given number of iterations using the supplied parameters.
    """

    def __init__(self, mdp, discount=0.9, iterations=100, theta=1e-5):
        """
        Your prioritized sweeping value iteration agent should take an mdp on
        construction, run the indicated number of iterations,
        and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        from collections import defaultdict

        def computeValueOfState(state):
            """
            Computes what the value of a state should be by returning maximum of Q-values
            """
            return max(
                ValueIterationAgent.computeQValueFromValues(self, state, action)
                for action in self.mdp.getPossibleActions(state)
            )

        # find predecessor for each state
        predecessors = defaultdict(set)
        for from_state in self.mdp.getStates():
            for action in self.mdp.getPossibleActions(from_state):
                for to_state, prob in self.mdp.getTransitionStatesAndProbs(
                    from_state, action
                ):
                    if prob != 0:
                        predecessors[to_state].add(from_state)

        # Initialize empty Priority Queue
        queue = util.PriorityQueue()

        # 标记所有non-terminal states为待更新
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                diff = abs(computeValueOfState(state) - self.values[state])
                queue.update(state, -diff)

        # 更新queue中states到正确值
        for _ in range(self.iterations):
            if queue.isEmpty():
                break
            state = queue.pop()  # state一定不会是终点
            self.values[state] = computeValueOfState(state)
            for predecessor in predecessors[state]:
                # 标记predecessor为待更新
                diff = abs(computeValueOfState(predecessor) - self.values[predecessor])
                if diff > self.theta:
                    queue.update(predecessor, -diff)
