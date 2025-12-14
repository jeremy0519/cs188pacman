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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # 第一种写法：DFS (Iterative)
    visited = set()
    stack = util.Stack()  # 队列的值形为(坐标(1,2), 到这个点的路径('L','R','L'))
    stack.push((problem.getStartState(), []))  # 初始化 起点入队
    while not stack.isEmpty():
        now = stack.pop()

        # *** *** *** *** *** ***
        visited.add(now[0])  # 注意了 When to mark visit? At pop
        # *** *** *** *** *** ***

        if problem.isGoalState(now[0]):
            # 到达终点
            return now[1]
        for nbr in problem.getSuccessors(now[0]):
            if nbr[0] in visited:
                continue
            stack.push((nbr[0], now[1] + [nbr[1]]))
    print("dfs找不到路")
    return []  # 找不到路

    # 第二种写法 DFS (Recursive)
    # visited = set()
    # path = []

    # def dfs(node):
    #     visited.add(node)  # 同上 When to mark visited? At pop
    #     if problem.isGoalState(node):
    #         # 到达终点
    #         return True
    #     for nbr in problem.getSuccessors(node):
    #         if nbr[0] in visited:
    #             continue
    #         path.append(nbr[1])  # 添加到这个点的路
    #         if dfs(nbr[0]):
    #             return True  # True代表已经找到，此时True会一层一层往上propogate，都会return True，不会执行后面的pop(-1)
    #         path.pop(-1)  # 这个点下面的所有都return了False，因此一定没法到终点，path里删去这个点
    #     return False  # 没法到达终点，这个False会被上层使用

    # dfs(problem.getStartState())
    # return path
    util.raiseNotDefined()


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    visited = set(problem.getStartState())  # 初始化 起点已经visit
    queue = util.Queue()  # 队列的值形为(坐标(1,2), 到这个点的路径('L','R','L'))
    queue.push((problem.getStartState(), []))  # 初始化 起点入队
    while not queue.isEmpty():
        now = queue.pop()
        if problem.isGoalState(now[0]):
            # 到达终点
            return now[1]
        for nbr in problem.getSuccessors(now[0]):
            if nbr[0] in visited:
                continue

            # *** *** *** *** *** ***
            visited.add(nbr[0])  # When mark visit? At push
            # *** *** *** *** *** ***

            queue.push((nbr[0], now[1] + [nbr[1]]))
    print("bfs找不到路")
    return []  # 找不到路

    util.raiseNotDefined()


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    from collections import defaultdict

    visited = set()
    backward_cost = defaultdict(int)  # 记录这个点的priority
    paths = defaultdict(int)  # 记录到这个点的路径
    backward_cost[problem.getStartState()] = 0
    paths[problem.getStartState()] = []
    priorityqueue = util.PriorityQueue()  # 优先队列只存坐标: Tuple
    priorityqueue.push(item=problem.getStartState(), priority=0)  # 初始化 起点入队
    while not priorityqueue.isEmpty():
        now = priorityqueue.pop()
        visited.add(now)  ##### mark visited at pop
        # print("now=", now)
        if problem.isGoalState(now):  # 到达终点
            return paths[now]
        for nbr in problem.getSuccessors(now):
            if nbr[0] in visited:
                continue
            if nbr[0] in backward_cost:  # priority字典里得有nbr.coordinates才有的比
                if (
                    backward_cost[now] + nbr[2] < backward_cost[nbr[0]]
                ):  # 新priority更小，需要更新
                    backward_cost[nbr[0]] = backward_cost[now] + nbr[2]
                    paths[nbr[0]] = paths[now] + [nbr[1]]  # paths同步也要更新
            else:
                backward_cost[nbr[0]] = (
                    backward_cost[now] + nbr[2]
                )  # 没得比，只能是从now走过来
                paths[nbr[0]] = paths[now] + [nbr[1]]
            priorityqueue.update(item=nbr[0], priority=backward_cost[nbr[0]])
    print("ucs找不到路")
    return []  # 找不到路
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from collections import defaultdict

    visited = set()
    backward_cost = defaultdict(int)  # 记录这个点的priority
    paths = defaultdict(int)  # 记录到这个点的路径
    backward_cost[problem.getStartState()] = 0
    paths[problem.getStartState()] = []
    priorityqueue = (
        util.PriorityQueue()
    )  # 优先队列只存坐标: Tuple, 到这个点的路径和cumulative cost都不存
    priorityqueue.push(
        item=problem.getStartState(),
        priority=0 + heuristic(problem.getStartState(), problem),
    )  # 初始化 起点入队
    while not priorityqueue.isEmpty():
        now = priorityqueue.pop()
        visited.add(now)  ##### mark visited at pop
        # print("now=", now)
        if problem.isGoalState(now):
            # 到达终点
            return paths[now]
        for nbr in problem.getSuccessors(now):
            if nbr[0] in visited:
                continue
            if nbr[0] in backward_cost:  # priority字典里有nbr.coordinates才有的比
                if (
                    backward_cost[now] + nbr[2] < backward_cost[nbr[0]]
                ):  # 新priority更小，需要更新
                    backward_cost[nbr[0]] = backward_cost[now] + nbr[2]
                    paths[nbr[0]] = paths[now] + [nbr[1]]  # paths同步更新
            else:
                backward_cost[nbr[0]] = (
                    backward_cost[now] + nbr[2]
                )  # 没得比，只能是从now走过来
                paths[nbr[0]] = paths[now] + [nbr[1]]
            priorityqueue.update(
                item=nbr[0], priority=backward_cost[nbr[0]] + heuristic(nbr[0], problem)
            )
    print("ucs找不到路")
    return []  # 找不到路
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
